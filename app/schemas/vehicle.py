"""Schémas des véhicules d'occasion"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.enums import VehicleStatus, FuelType, TransmissionType
from app.schemas.image import VehicleImageRead


class VehicleCreate(BaseModel):
    title: str
    brand: str
    model: str
    year: int = Field(ge=1900, le=2100)
    mileage: int = Field(ge=0)
    fuel: FuelType
    transmission: TransmissionType
    price: int = Field(ge=0)
    description: str


class VehicleUpdate(BaseModel):
    title: str | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = Field(default=None, ge=1900, le=2100)
    mileage: int | None = Field(default=None, ge=0)
    fuel: FuelType | None = None
    transmission: TransmissionType | None = None
    price: int | None = Field(default=None, ge=0)
    description: str | None = None
    status: VehicleStatus | None = None
    is_featured: bool | None = None
    is_published: bool | None = None


class VehicleRead(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    mileage: int
    fuel: FuelType
    transmission: TransmissionType
    price: int
    description: str
    status: VehicleStatus
    is_featured: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    images: list[VehicleImageRead] = []

    model_config = ConfigDict(from_attributes=True)


class PublicVehicleRead(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    mileage: int
    fuel: FuelType
    transmission: TransmissionType
    price: int
    description: str
    status: VehicleStatus
    images: list[VehicleImageRead] = []

    model_config = ConfigDict(from_attributes=True)
