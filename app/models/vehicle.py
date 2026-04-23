"""Table des véhicules en vente"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from app.enums import VehicleStatus, FuelType, TransmissionType


class Vehicle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    brand: str
    model: str
    year: int
    mileage: int
    fuel: FuelType = Field(default=FuelType.PETROL)
    transmission: TransmissionType = Field(default=TransmissionType.MANUAL)
    price: int
    description: str
    status: VehicleStatus = Field(default=VehicleStatus.AVAILABLE)
    is_featured: bool = Field(default=True)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    images: list["VehicleImage"] = Relationship(back_populates="vehicle")


class VehicleImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image_url: str
    is_cover: bool = Field(default=False)
    display_order: int = Field(default=0)
    alt_text: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    vehicle_id: int = Field(foreign_key="vehicle.id", index=True)
    vehicle: Vehicle = Relationship(back_populates="images")
