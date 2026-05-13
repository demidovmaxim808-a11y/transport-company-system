from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.models.trip import Trip, TripStatus
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class TripRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, trip_id: int) -> Optional[Trip]:
        return self.db.query(Trip).options(
            joinedload(Trip.driver),
            joinedload(Trip.trailer),
            joinedload(Trip.route)
        ).filter(Trip.id == trip_id).first()
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[Trip]:
        query = self.db.query(Trip)
        
        if filters:
            if 'driver_id' in filters:
                query = query.filter(Trip.driver_id == filters['driver_id'])
            query = apply_filters(query, Trip, {k: v for k, v in filters.items() if k != 'driver_id'})
        
        total = query.count()
        
        query = apply_sorting(query, Trip, sort_by, sort_order)
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)
    
    def get_active_trips(self) -> List[Trip]:
        return self.db.query(Trip).filter(
            Trip.status == TripStatus.IN_PROGRESS
        ).all()
    
    def get_driver_trips(self, driver_id: int, page: int = 1, size: int = 20) -> PaginatedResults[Trip]:
        query = self.db.query(Trip).filter(Trip.driver_id == driver_id)
        total = query.count()
        query = apply_pagination(query, page, size)
        items = query.all()
        return PaginatedResults(items, total, page, size)
    
    def create(self, trip_data: dict) -> Trip:
        trip = Trip(**trip_data)
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip
    
    def update(self, trip: Trip, update_data: dict) -> Trip:
        for key, value in update_data.items():
            if hasattr(trip, key) and value is not None:
                setattr(trip, key, value)
        
        self.db.commit()
        self.db.refresh(trip)
        return trip
    
    def delete(self, trip: Trip) -> None:
        self.db.delete(trip)
        self.db.commit()
    
    def get_trips_in_period(self, start_date: datetime, end_date: datetime) -> List[Trip]:
        return self.db.query(Trip).filter(
            Trip.created_at >= start_date,
            Trip.created_at <= end_date
        ).all()