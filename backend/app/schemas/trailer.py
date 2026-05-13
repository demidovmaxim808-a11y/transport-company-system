from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TrailerBase(BaseModel):
    model: str = Field(..., min_length=1, max_length=150)
    plate_number: str = Field(..., min_length=1, max_length=20)
    capacity: float = Field(..., gt=0)
    status: Optional[str] = "available"


class TrailerCreate(TrailerBase):
    pass


class TrailerUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=1, max_length=150)
    plate_number: Optional[str] = Field(None, min_length=1, max_length=20)
    capacity: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None


class TrailerResponse(TrailerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TrailerListResponse(BaseModel):
    items: list[TrailerResponse]
    total: int
    page: int
    size: int
    pages: int