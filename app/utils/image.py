from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.vehicle import VehicleImage
from app.models.part import PartImage


def get_vehicle_image_or_404(
    session: Session, vehicle_id: int, image_id: int
) -> VehicleImage:
    statement = select(VehicleImage).where(
        VehicleImage.id == image_id,
        VehicleImage.vehicle_id == vehicle_id,
    )

    image = session.exec(statement).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image introuvable")
    return image


def get_part_image_or_404(session: Session, part_id: int, image_id: int) -> PartImage:

    statement = select(PartImage).where(
        PartImage.id == image_id,
        PartImage.part_id == part_id,
    )

    image = session.get(statement).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image introuvable")
    return image
