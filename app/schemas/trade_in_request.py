from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TradeInRequestCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    brand: str
    model: str
    year: int = Field(ge=1900, le=2100)
    mileage: int = Field(ge=0)
    condition_note: str
    message: str


class TradeInRequestRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    brand: str
    model: str
    year: int
    mileage: int
    condition_note: str
    message: str
    created_at: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)


class TradeInRequestUpdate(BaseModel):
    is_read: bool | None = None
