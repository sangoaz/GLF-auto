from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class TradeInRequestCreate(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr
    phone: str = Field(max_length=20)
    brand: str = Field(max_length=100)
    model: str = Field(max_length=100)
    year: int = Field(ge=1900, le=2100)
    mileage: int = Field(ge=0)
    condition_note: str = Field(max_length=1000)
    message: str = Field(max_length=2000)


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
