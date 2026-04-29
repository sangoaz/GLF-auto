"""Routes publiques relatives aux services proposés"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, Session

from app.core.database import get_session
from app.models.service import Service
from app.schemas.service import PublicServiceRead

router = APIRouter(prefix="/services", tags=["Public Services"])


# Liste des services proposés
@router.get("/", response_model=list[PublicServiceRead])
def list_public_services(
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(Service)
        .where(Service.is_active == True)
        .order_by(Service.display_order)
        .offset(offset)
        .limit(limit)
    )

    services = session.exec(statement).all()
    return services


# Afficher la page d'un seul service
@router.get("/{service_id}", response_model=PublicServiceRead)
def get_public_service(
    service_id: int,
    session: Session = Depends(get_session),
):
    statement = select(Service).where(
        Service.id == service_id,
        Service.is_active == True,
    )

    service = session.exec(statement).first()

    if not service:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    return service
