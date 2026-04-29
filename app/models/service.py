"""Table des services proposés"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    short_description: str
    full_description: str
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
