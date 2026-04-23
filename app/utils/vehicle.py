from fastapi import HTTPException
from sqlmodel import Session

from app.enums import UserRole
from app.models.vehicle import Vehicle


def get_vehicle_or_404(session: Session, vehicle_id: int) -> Vehicle:
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")
    return vehicle
