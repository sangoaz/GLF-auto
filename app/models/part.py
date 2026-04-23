"""Table des pièces d'occasion en ventes"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from app.enums import PartStatus


class Part(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    category: str
    brand: str
    compatible_models: str
    condition: str
    price: int
    description: str
    status: PartStatus = Field(default=PartStatus.AVAILABLE)
    is_featured: bool = Field(default=True)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    images: list["PartImage"] = Relationship(back_populates="part")


class PartImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    image_url: str
    is_cover: bool = Field(default=False)
    display_order: int = Field(default=0)
    alt_text: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    part_id: int = Field(foreign_key="part.id", index=True)
    part: Part = Relationship(back_populates="images")
