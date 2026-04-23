"""Table des demandes de reprise de véhicules"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class TradeInRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    brand: str
    model: str
    year: int
    mileage: int
    condition_note: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_read: bool = Field(default=False)
