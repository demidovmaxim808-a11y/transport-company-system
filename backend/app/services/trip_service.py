from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.trip_repository import TripRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException
from app.core.logger import logger
from app.schemas.trip import TripCreate, TripUpdate, TripResponse, TripListResponse


class TripService:
    def __init__(self, db: Session):
        self.trip_repo = TripRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_trips(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> TripListResponse:
        result = self.trip_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return TripListResponse(
            items=[TripResponse.model_validate(trip) for trip in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_trip_by_id(self, trip_id: int) -> TripResponse:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")
        return TripResponse.model_validate(trip)
    
    def create_trip(self, trip_data: TripCreate, current_user: User) -> TripResponse:
        trip = self.trip_repo.create(trip_data.model_dump())
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="CREATE",
            entity_name="Trip",
            entity_id=trip.id,
            details=f"Trip created for driver {trip.driver_id}"
        )
        
        logger.info(f"Trip created: ID {trip.id}")
        
        return TripResponse.model_validate(trip)
    
    def update_trip(self, trip_id: int, update_data: TripUpdate, current_user: User) -> TripResponse:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_trip = self.trip_repo.update(trip, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="Trip",
            entity_id=trip_id,
            details=f"Trip updated"
        )
        
        logger.info(f"Trip updated: ID {trip_id}")
        
        return TripResponse.model_validate(updated_trip)
    
    def delete_trip(self, trip_id: int, current_user: User) -> None:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip:
            raise NotFoundException("Trip not found")
        
        self.trip_repo.delete(trip)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="Trip",
            entity_id=trip_id,
            details=f"Trip deleted"
        )
        
        logger.info(f"Trip deleted: ID {trip_id}")
    
    def get_my_trips(self, driver_id: int, page: int = 1, size: int = 20) -> TripListResponse:
        result = self.trip_repo.get_driver_trips(driver_id, page, size)
        
        return TripListResponse(
            items=[TripResponse.model_validate(trip) for trip in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )