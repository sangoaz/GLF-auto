"""Routes admin relatives aux véhicules d'occasion"""

from datetime import datetime, timezone
from fastapi import APIRouter, Query, Depends, File, UploadFile, Form
from sqlmodel import select, Session
from typing import List


from app.core.database import get_session
from app.deps.auth import require_admin
from app.enums import VehicleStatus
from app.models.vehicle import Vehicle, VehicleImage
from app.models.user import User
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)
from app.schemas.image import (
    VehicleImageCreate,
    VehicleImageRead,
    VehicleImageUpdate,
)
from app.services.file_storage import save_uploaded_image, delete_uploaded_file
from app.services.image_service import (
    insert_image_with_order,
    delete_image_with_reindex,
    set_cover_image,
    reorder_image,
)
from app.utils.vehicle import get_vehicle_or_404
from app.utils.image import get_vehicle_image_or_404


router = APIRouter(prefix="/admin", tags=["Vehicles"])

# =====================
#   Véhicules
# =====================


# Enregistrer une nouvelle annonce de véhicule
@router.post("/vehicles", status_code=201, response_model=VehicleRead)
def create_vehicle(
    vehicle: VehicleCreate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    # model_dump permet d'éviter de recopier tous les champs du VehicleCreate
    new_vehicle = Vehicle(**vehicle.model_dump())

    session.add(new_vehicle)
    session.commit()
    session.refresh(new_vehicle)

    return new_vehicle


# Liste des véhicules en vente
@router.get("/vehicles", response_model=List[VehicleRead])
def list_vehicles(
    admin_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):

    statement = (
        select(Vehicle).order_by(Vehicle.created_at.desc()).offset(offset).limit(limit)
    )

    vehicles = session.exec(statement).all()

    return vehicles


# Afficher une annonce de véhicule
@router.get("/vehicles/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(
    vehicle_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    vehicle = get_vehicle_or_404(session, vehicle_id)

    return vehicle


# Update une annonce de véhicule
@router.patch("/vehicles/{vehicle_id}", response_model=VehicleRead)
def patch_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):

    existing_vehicle = get_vehicle_or_404(session, vehicle_id)

    # Permet de ne pas écrire tous les champs de VehiculeUpdate
    update_data = vehicle.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_vehicle, field, value)

    # Si modification du statut en RESERVED, arrêt de la mise en avant de l'annonce
    if existing_vehicle.status == VehicleStatus.RESERVED:
        existing_vehicle.is_featured = False

    # Si modification du statut en SOLD, dépublication de l'annonce
    if existing_vehicle.status == VehicleStatus.SOLD:
        existing_vehicle.is_featured = False
        existing_vehicle.is_published = False

    existing_vehicle.updated_at = datetime.now(timezone.utc)

    session.commit()
    session.refresh(existing_vehicle)

    return existing_vehicle


# =====================
#   Images
# =====================


# Afficher la liste des images de la pièce détachée
@router.get("/vehicles/{vehicle_id}/images", response_model=List[VehicleImageRead])
def list_vehicle_images(
    vehicle_id: int,
    admin_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    limit: int = Query(default=10, le=15),
    offset: int = Query(default=0, ge=0),
):

    vehicle = get_vehicle_or_404(session, vehicle_id)

    statement = (
        select(VehicleImage)
        .where(VehicleImage.vehicle_id == vehicle_id)
        .order_by(VehicleImage.display_order)
        .offset(offset)
        .limit(limit)
    )

    vehicle_images = session.exec(statement).all()

    return vehicle_images


# Modifier la photo de couverture de l'annonce
@router.patch(
    "/vehicles/{vehicle_id}/images/{image_id}/cover", response_model=VehicleImageRead
)
def set_vehicle_cover(
    vehicle_id: int,
    image_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    vehicle = get_vehicle_or_404(session, vehicle_id)
    vehicle_image = get_vehicle_image_or_404(session, vehicle_id, image_id)

    set_cover_image(
        session=session,
        image_model=VehicleImage,
        parent_field="vehicle_id",
        parent_id=vehicle.id,
        target_image=vehicle_image,
    )

    session.commit()
    session.refresh(vehicle_image)

    return vehicle_image


# Modificer les infos de l'image comme le alt_text ou l'ordre d'affichage
@router.patch(
    "/vehicles/{vehicle_id}/images/{image_id}", response_model=VehicleImageRead
)
def update_vehicle_image(
    vehicle_id: int,
    image_id: int,
    image: VehicleImageUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    vehicle = get_vehicle_or_404(session, vehicle_id)
    vehicle_image = get_vehicle_image_or_404(session, vehicle_id, image_id)

    update_data = image.model_dump(exclude_unset=True)

    if "alt_text" in update_data:
        vehicle_image.alt_text = update_data["alt_text"]

    if "display_order" in update_data:
        reorder_image(
            session=session,
            image_model=VehicleImage,
            parent_field="vehicle_id",
            parent_id=vehicle.id,
            target_image=vehicle_image,
            new_order=update_data["display_order"],
        )

    session.commit()
    session.refresh(vehicle_image)

    return vehicle_image


# =====================
#   Fichiers Images
# =====================


# Upload une image
@router.post(
    "/vehicles/{vehicle_id}/images/upload",
    response_model=VehicleImageRead,
    status_code=201,
)
def upload_vehicle_image(
    vehicle_id: int,
    file: UploadFile = File(...),
    display_order: int = Form(0),
    alt_text: str | None = Form(None),
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    vehicle = get_vehicle_or_404(session, vehicle_id)

    image_path = save_uploaded_image(
        file=file,
        subfolder="vehicles",
    )

    new_image = VehicleImage(
        image_url=image_path,
        display_order=display_order,
        alt_text=alt_text,
        vehicle_id=vehicle.id,
    )

    insert_image_with_order(
        session=session,
        image_model=VehicleImage,
        parent_field="vehicle_id",
        parent_id=vehicle.id,
        new_image=new_image,
    )

    session.commit()
    session.refresh(new_image)

    return new_image


# Supprimer une image de l'annonce
@router.delete("/vehicles/{vehicle_id}/images/{image_id}")
def delete_vehicle_image(
    vehicle_id: int,
    image_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    vehicle = get_vehicle_or_404(session, vehicle_id)
    vehicle_image = get_vehicle_image_or_404(session, vehicle_id, image_id)

    image_url = vehicle_image.image_url

    delete_image_with_reindex(
        session=session,
        image_model=VehicleImage,
        parent_field="vehicle_id",
        parent_id=vehicle.id,
        target_image=vehicle_image,
    )

    session.commit()

    delete_uploaded_file(image_url)

    return {"message": f"L'image {image_id} a été supprimé"}
