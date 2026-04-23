"""Routes publiques relatives aux véhicules d'occasion"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, Session

from app.core.database import get_session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import PublicVehicleRead

router = APIRouter(prefix="/vehicles", tags=["Public Vehicles"])


# Liste des véhicules en vente ou réservés
@router.get("/", response_model=list[PublicVehicleRead])
def list_public_vehicles(
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=20),
    offset: int = Query(default=0, ge=0),
):
    statement = (
        select(Vehicle)
        .where(Vehicle.is_published == True)
        .order_by(Vehicle.is_featured.desc(), Vehicle.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    vehicles = session.exec(statement).all()
    return vehicles


# Afficher l'annonce d'un seul véhicule
@router.get("/{vehicle_id}", response_model=PublicVehicleRead)
def get_public_vehicle(
    vehicle_id: int,
    session: Session = Depends(get_session),
):
    statement = select(Vehicle).where(
        Vehicle.id == vehicle_id,
        Vehicle.is_published == True,
    )

    vehicle = session.exec(statement).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    return vehicle
