from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    cargo_type: str = Field(..., min_length=1, max_length=150)
    cargo_weight: float = Field(..., gt=0)
    trip_id: Optional[int] = None
    status: Optional[str] = "pending"
    price: Optional[float] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255)
    cargo_type: Optional[str] = Field(None, min_length=1, max_length=150)
    cargo_weight: Optional[float] = Field(None, gt=0)
    trip_id: Optional[int] = None
    status: Optional[str] = None
    price: Optional[float] = None


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    size: int
    pages: int