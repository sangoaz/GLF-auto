"""Schémas des pièces d'occasion"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.enums import PartStatus, PartCondition
from app.schemas.image import PartImageRead


class PartCreate(BaseModel):
    title: str
    category: str
    brand: str
    compatible_models: str
    condition: PartCondition
    price: int
    description: str


class PartUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    brand: str | None = None
    compatible_models: str | None = None
    condition: PartCondition | None = None
    price: int | None = Field(default=None, ge=0)
    description: str | None = None
    status: PartStatus | None = None
    is_featured: bool | None = None
    is_published: bool | None = None


class PartRead(BaseModel):
    id: int
    title: str
    category: str
    brand: str
    compatible_models: str
    condition: PartCondition
    price: int
    description: str
    status: PartStatus
    is_featured: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    images: list[PartImageRead] = []

    model_config = ConfigDict(from_attributes=True)


class PublicPartRead(BaseModel):
    id: int
    title: str
    category: str
    brand: str
    compatible_models: str
    condition: PartCondition
    price: int
    description: str
    status: PartStatus
    images: list[PartImageRead] = []

    model_config = ConfigDict(from_attributes=True)
