from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class ContactRequestCreate(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr
    phone: str = Field(max_length=20)
    subject: str = Field(max_length=200)
    message: str = Field(max_length=2000)


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
