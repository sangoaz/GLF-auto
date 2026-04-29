"""Schémas des services proposés"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ServiceCreate(BaseModel):
    title: str
    short_description: str
    full_description: str
    display_order: int | None = Field(default=None, ge=0)


class ServiceUpdate(BaseModel):
    title: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ServiceRead(BaseModel):
    id: int
    title: str
    short_description: str
    full_description: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicServiceRead(BaseModel):
    id: int
    title: str
    short_description: str
    full_description: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)
