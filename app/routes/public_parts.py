"""Routes publiques relatives aux pièces d'occasion"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, Session

from app.core.database import get_session
from app.models.part import Part
from app.schemas.part import PublicPartRead

router = APIRouter(prefix="/parts", tags=["Public Parts"])


# Liste des pièces d'occasion en vente ou réservées

# Afficher l'annnonce d'une seule pièce
