from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RouteBase(BaseModel):
    departure_point: str = Field(..., min_length=1, max_length=255)
    destination_point: str = Field(..., min_length=1, max_length=255)
    distance_km: float = Field(..., gt=0)


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    departure_point: Optional[str] = Field(None, min_length=1, max_length=255)
    destination_point: Optional[str] = Field(None, min_length=1, max_length=255)
    distance_km: Optional[float] = Field(None, gt=0)


class RouteResponse(RouteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RouteListResponse(BaseModel):
    items: list[RouteResponse]
    total: int
    page: int
    size: int
    pages: int