from fastapi import HTTPException
from sqlmodel import Session

from app.models.contact_request import ContactRequest
from app.models.trade_in_request import TradeInRequest


def get_contact_request_or_404(
    session: Session, contact_request_id: int
) -> ContactRequest:
    contact_request = session.get(ContactRequest, contact_request_id)
    if not contact_request:
        raise HTTPException(status_code=404, detail="Demande de contact introuvable")
    return contact_request


def get_trade_in_request_or_404(
    session: Session, trade_in_request_id: int
) -> TradeInRequest:
    trade_in_request = session.get(TradeInRequest, trade_in_request_id)
    if not trade_in_request:
        raise HTTPException(
            status_code=404, detail="Demande de reprise de véhicule introuvable"
        )
    return trade_in_request
