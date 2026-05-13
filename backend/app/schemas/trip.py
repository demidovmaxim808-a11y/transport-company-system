from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TripBase(BaseModel):
    driver_id: int
    trailer_id: int
    route_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    status: Optional[str] = "planned"


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    driver_id: Optional[int] = None
    trailer_id: Optional[int] = None
    route_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class TripResponse(TripBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TripListResponse(BaseModel):
    items: list[TripResponse]
    total: int
    page: int
    size: int
    pages: int


class TripDetailResponse(TripResponse):
    driver_name: Optional[str] = None
    trailer_plate: Optional[str] = None
    route_info: Optional[str] = None