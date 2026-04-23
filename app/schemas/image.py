"""Schémas des images pour les véhicules d'occasion, et les pièces auto"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class VehicleImageCreate(BaseModel):
    image_url: str
    display_order: int | None = Field(default=None, ge=0)
    alt_text: str | None = None


class VehicleImageRead(BaseModel):
    id: int
    image_url: str
    is_cover: bool
    display_order: int
    alt_text: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VehicleImageUpdate(BaseModel):
    display_order: int | None = Field(default=0, ge=0)
    alt_text: str | None = None


class PartImageCreadte(BaseModel):
    image_url: str
    display_order: int | None = Field(default=None, ge=0)
    alt_text: str | None = None


class PartImageRead(BaseModel):
    id: int
    image_url: str
    is_cover: bool
    display_order: int
    alt_text: str | None = None
    created_at: datetime


class PartImageUpdate(BaseModel):
    display_order: int | None = Field(default=0, ge=0)
    alt_text: str | None = None
