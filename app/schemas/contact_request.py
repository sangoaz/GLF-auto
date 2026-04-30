from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class ContactRequestCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    subject: str
    message: str


class ContactRequestRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    subject: str
    message: str
    created_at: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)


class ContactRequestUpdate(BaseModel):
    is_read: bool | None = None
