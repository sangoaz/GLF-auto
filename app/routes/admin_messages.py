"""Routes admin relatives aux messages reçus"""

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.deps.auth import require_admin
from app.models.trade_in_request import TradeInRequest
from app.models.contact_request import ContactRequest
from app.models.user import User
from app.schemas.contact_request import ContactRequestRead, ContactRequestUpdate
from app.schemas.trade_in_request import TradeInRequestRead, TradeInRequestUpdate
from app.utils.messages import (
    get_contact_request_or_404,
    get_trade_in_request_or_404,
)

router = APIRouter(prefix="/admin", tags=["Messages"])


@router.get("/contact-requests", response_model=list[ContactRequestRead])
def list_contact_requests(
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
    limit: int = Query(default=20, le=50),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(ContactRequest)
        .order_by(ContactRequest.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


@router.get("/contact-requests/{request_id}", response_model=ContactRequestRead)
def get_contact_request(
    request_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    return get_contact_request_or_404(session, request_id)


@router.patch("/contact-requests/{request_id}", response_model=ContactRequestRead)
def patch_contact_request(
    request_id: int,
    contact_update: ContactRequestUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    contact_request = get_contact_request_or_404(session, request_id)

    update_data = contact_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(contact_request, field, value)

    session.commit()
    session.refresh(contact_request)

    return contact_request


@router.get("/trade-in-requests", response_model=list[TradeInRequestRead])
def list_trade_in_requests(
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
    limit: int = Query(default=20, le=50),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(TradeInRequest)
        .order_by(TradeInRequest.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    return session.exec(statement).all()


@router.get("/trade-in-requests/{request_id}", response_model=TradeInRequestRead)
def get_trade_in_request(
    request_id: int,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    return get_trade_in_request_or_404(session, request_id)


@router.patch("/trade-in-requests/{request_id}", response_model=TradeInRequestRead)
def patch_trade_in_request(
    request_id: int,
    trade_in_update: TradeInRequestUpdate,
    session: Session = Depends(get_session),
    admin_user: User = Depends(require_admin),
):
    trade_in_request = get_trade_in_request_or_404(session, request_id)

    update_data = trade_in_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(trade_in_request, field, value)

    session.commit()
    session.refresh(trade_in_request)

    return trade_in_request
