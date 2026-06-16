"""Routes publiques relatives aux demandes de reprise"""

from fastapi import APIRouter, Depends
from sqlmodel import Session
import logging

from app.core.database import get_session
from app.models.trade_in_request import TradeInRequest
from app.schemas.trade_in_request import TradeInRequestCreate, TradeInRequestRead

from app.services.email_service import send_trade_in_notification

router = APIRouter(prefix="/trade-in", tags=["Public Trade In"])

logger = logging.getLogger(__name__)


@router.post("", response_model=TradeInRequestRead, status_code=201)
def create_trade_in_request(
    trade_in: TradeInRequestCreate,
    session: Session = Depends(get_session),
):
    new_trade_in = TradeInRequest(**trade_in.model_dump())

    session.add(new_trade_in)
    session.commit()
    session.refresh(new_trade_in)

    try:
        send_trade_in_notification(new_trade_in)
        logger.info("Email contact envoyé avec succès")
    except Exception:
        logger.exception("Erreur lors de l'envoi de l'email de trade in request")

    return new_trade_in
