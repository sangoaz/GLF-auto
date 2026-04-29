"""Routes publiques relatives aux pièces d'occasion"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, Session

from app.core.database import get_session
from app.models.part import Part
from app.schemas.part import PublicPartRead

router = APIRouter(prefix="/parts", tags=["Public Parts"])


# Liste des pièces d'occasion en vente ou réservées
@router.get("/", response_model=list[PublicPartRead])
def list_public_parts(
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(Part)
        .where(Part.is_published == True)
        .order_by(Part.is_featured.desc(), Part.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    parts = session.exec(statement).all()
    return parts


# Afficher l'annnonce d'une seule pièce
@router.get("/{part_id}", response_model=PublicPartRead)
def get_public_part(
    part_id: int,
    session: Session = Depends(get_session),
):
    statement = select(Part).where(
        Part.id == part_id,
        Part.is_published == True,
    )

    part = session.exec(statement).first()

    if not part:
        raise HTTPException(status_code=404, detail="Pièce introuvable")

    return part
