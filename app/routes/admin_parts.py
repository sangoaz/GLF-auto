"""Routes admin relatives aux pièces détachées d'occasion"""

from datetime import datetime, timezone
from fastapi import APIRouter, Query, Depends, File, UploadFile, Form
from sqlmodel import select, Session


from app.core.database import get_session
from app.deps.auth import require_admin
from app.enums import PartStatus
from app.models.part import Part, PartImage
from app.models.user import User
from app.schemas.part import (
    PartCreate,
    PartRead,
    PartUpdate,
)
from app.schemas.image import (
    PartImageCreadte,
    PartImageRead,
    PartImageUpdate,
)
from app.services.file_storage import save_uploaded_image, delete_uploaded_file
from app.services.image_service import (
    insert_image_with_order,
    delete_image_with_reindex,
    set_cover_image,
    reorder_image,
)
from app.utils.part import get_part_or_404
from app.utils.image import get_part_image_or_404


router = APIRouter(prefix="/admin", tags=["Parts"])

# =====================
#   Pièces détachées
# =====================


# Enregistrer une nouvelle annonce de pièce détachée
@router.get("/parts", status_code=201, response_model=PartRead)
def create_part(
    part: PartCreate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    new_part = Part(**part.model_dump())

    session.add(part)
    session.commit()
    session.refresh(new_part)


# Liste des pièces en vente
@router.get("/parts", response_model=list[PartRead])
def list_parts(
    admin_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):

    statement = (
        select(Part).order_by(Part.created_at.desc()).offset(offset).limit(limit)
    )

    parts = session.exec(statement).all()

    return parts


# Afficher une annonce de pièce
@router.get("/parts/{part_id}", response_model=PartRead)
def get_part(
    part_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    part = get_part_or_404(session, part_id)

    return part


# Update une annnonce de pièce
@router.patch("/parts/{part_id}", response_model=PartRead)
def patch_part(
    part_id: int,
    part: PartUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):

    existing_part = get_part_or_404(session, part_id)

    update_data = part.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_part, field, value)

    if existing_part.status == PartStatus.RESERVED:
        existing_part.is_featured = False

    if existing_part.status == PartStatus.SOLD:
        existing_part.is_featured = False
        existing_part.is_published = False

    existing_part.updated_at = datetime.now(timezone.utc)


# =====================
#   Images
# =====================


# Afficher la liste des images de la pièce détachée
@router.get("/parts/{part_id}/images", response_model=list[PartImageRead])
def list_part_images(
    part_id: int,
    admin_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    limit: int = Query(default=5, le=10),
    offset: int = Query(default=0, ge=0),
):

    part = get_part_or_404(session, part_id)

    statement = (
        select(PartImage)
        .where(PartImage.part_id == part_id)
        .order_by(PartImage.display_order)
        .offset(offset)
        .limit(limit)
    )

    part_image = session.exec(statement).all()

    return part_image


# Modifier la photo de couverture de l'annonce
@router.patch("/part/{part_id}/images/{image_id}/cover", response_model=PartImageRead)
def set_part_cover(
    part_id: int,
    image_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    part = get_part_or_404(session, part_id)
    part_image = get_part_image_or_404(session, part_id, image_id)

    set_cover_image(
        session=session,
        image_model=PartImage,
        parent_field="part_id",
        parent_id=part.id,
        target_image=part_image,
    )

    session.commit()
    session.refresh(part_image)

    return part_image


# Modificer les infos de l'image comme le alt_text ou l'ordre d'affichage
@router.patch("/parts/{part_id}/images/{image_id}", response_model=PartImageRead)
def update_part_image(
    part_id: int,
    image_id: int,
    image: PartImageUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    part = get_part_or_404(session, part_id)
    part_image = get_part_image_or_404(session, part_id, image_id)

    update_data = image.model_dump(exclude_unset=True)

    if "alt_text" in update_data:
        part_image.alt_text = update_data["alt_text"]

    if "display_order" in update_data:
        reorder_image(
            session=session,
            image_model=PartImage,
            parent_field="part_id",
            parent_id=part.id,
            target_image=part_image,
            new_order=update_data["display_order"],
        )

    session.commit()
    session.refresh(part_image)

    return part_image


# =====================
#   Fichiers Images
# =====================


# Upload une image
@router.post(
    "/parts/{part_id}/images/upload",
    response_model=PartImageRead,
    status_code=201,
)
def upload_part_image(
    part_id: int,
    file: UploadFile = File(...),
    display_order: int = Form(0),
    alt_text: str | None = Form(None),
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    part = get_part_or_404(session, part_id)

    image_path = save_uploaded_image(
        file=file,
        subfolder="parts",
    )

    new_image = PartImage(
        image_url=image_path,
        display_order=display_order,
        alt_text=alt_text,
        part_id=part.id,
    )

    insert_image_with_order(
        session=session,
        image_model=PartImage,
        parent_field="part_id",
        parent_id=part.id,
        new_image=new_image,
    )

    session.commit()
    session.refresh(new_image)

    return new_image


# Supprimer une image de l'annonce
@router.delete("/parts/{part_id}/images/{image_id}")
def delete_part_image(
    part_id: int,
    image_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    part = get_part_or_404(session, part_id)
    part_image = get_part_image_or_404(session, part_id, image_id)

    image_url = part_image.image_url

    delete_image_with_reindex(
        session=session,
        image_model=PartImage,
        parent_field="part_id",
        parent_id=part.id,
        target_image=part_image,
    )

    session.commit()

    delete_uploaded_file(image_url)

    return {"message": f"L'image {image_id} a été supprimé"}
