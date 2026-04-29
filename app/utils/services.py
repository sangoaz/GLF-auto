from fastapi import HTTPException
from sqlmodel import Session

from app.models.service import Service


def get_service_or_404(session: Session, service_id: int) -> Service:
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service introuvable")
    return service
