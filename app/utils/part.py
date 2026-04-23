from fastapi import HTTPException
from sqlmodel import Session

from app.models.part import Part


def get_part_or_404(session: Session, part_id: int) -> Part:
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, détail="Pièce introuvable")
    return part
