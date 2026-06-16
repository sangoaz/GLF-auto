"""Routes publiques relatives aux demandes de contact"""

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
import logging

from app.core.database import get_session
from app.models.contact_request import ContactRequest
from app.schemas.contact_request import ContactRequestCreate, ContactRequestRead
from app.main import limiter

from app.services.email_service import send_contact_notification

router = APIRouter(prefix="/contact", tags=["Public Contact"])

logger = logging.getLogger(__name__)


@router.post("", response_model=ContactRequestRead, status_code=201)
@limiter.limit("5/minute")
def create_contact_request(
    request: Request,  # Obligatoire pour slowapi
    contact: ContactRequestCreate,
    session: Session = Depends(get_session),
):
    new_contact = ContactRequest(**contact.model_dump())

    session.add(new_contact)
    session.commit()
    session.refresh(new_contact)

    try:
        send_contact_notification(new_contact)
        logger.info("Email contact envoyé avec succès")
    except Exception:
        logger.exception("Erreur lors de l'envoi de l'email contact")

    return new_contact
