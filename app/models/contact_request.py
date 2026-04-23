"""Table des demandes du formulaire client"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class ContactRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    subject: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_read: bool = Field(default=False)
