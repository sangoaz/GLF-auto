"""Routes admin relative aux services proposés"""

from datetime import datetime, timezone
from fastapi import APIRouter, Query, Depends
from sqlmodel import select, Session

from app.core.database import get_session
from app.deps.auth import require_admin
from app.models.service import Service
from app.models.user import User
from app.schemas.service import (
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
)
from app.utils.services import get_service_or_404


router = APIRouter(prefix="/admin", tags=["Services"])


# =====================
#   Services
# =====================


# Enregistrer un nouveau service
@router.post("/services", status_code=201, response_model=ServiceRead)
def create_service(
    service: ServiceCreate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    # model_dump permet d'éviter de recopier tous les champs du ServiceCreate
    new_service = Service(**service.model_dump())

    session.add(new_service)
    session.commit()
    session.refresh(new_service)

    return new_service


# Liste des services proposés
@router.get("/services", response_model=list[ServiceRead])
def list_services(
    admin_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):

    statement = (
        select(Service).order_by(Service.created_at.desc()).offset(offset).limit(limit)
    )

    services = session.exec(statement).all()

    return services


# Afficher un service
@router.get("/services/{service_id}", response_model=ServiceRead)
def get_service(
    service_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    service = get_service_or_404(session, service_id)

    return service


# Update un services
@router.patch("/services/{service_id}", response_model=ServiceRead)
def patch_service(
    service_id: int,
    service: ServiceUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):

    existing_service = get_service_or_404(session, service_id)

    # Permet de ne pas écrire tous les champs de ServiceUpdate
    update_data = service.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_service, field, value)

    existing_service.updated_at = datetime.now(timezone.utc)

    session.commit()
    session.refresh(existing_service)

    return existing_service
