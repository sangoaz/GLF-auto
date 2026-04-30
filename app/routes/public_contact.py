"""Routes publiques relatives aux demandes de contact"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.models.contact_request import ContactRequest
from app.schemas.contact_request import ContactRequestCreate, ContactRequestRead

from app.services.email_service import send_contact_notification

router = APIRouter(prefix="/contact", tags=["Public Contact"])


@router.post("", response_model=ContactRequestRead, status_code=201)
def create_contact_request(
    contact: ContactRequestCreate,
    session: Session = Depends(get_session),
):
    new_contact = ContactRequest(**contact.model_dump())

    session.add(new_contact)
    session.commit()
    session.refresh(new_contact)

    try:
        send_contact_notification(new_contact)
    except:
        pass

    return new_contact
