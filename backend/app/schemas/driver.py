from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DriverBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    license_number: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=20)
    experience_years: float = Field(default=0, ge=0)
    status: Optional[str] = "available"


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    license_number: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    experience_years: Optional[float] = Field(None, ge=0)
    status: Optional[str] = None


class DriverResponse(DriverBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DriverListResponse(BaseModel):
    items: list[DriverResponse]
    total: int
    page: int
    size: int
    pages: int