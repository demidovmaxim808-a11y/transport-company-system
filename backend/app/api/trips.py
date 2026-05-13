from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager, all_roles
from app.models.user import User
from app.schemas.trip import TripCreate, TripUpdate, TripResponse, TripListResponse
from app.services.trip_service import TripService

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.get("/", response_model=TripListResponse)
def get_trips(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    status: Optional[str] = Query(None),
    driver_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    filters = {}
    if status:
        filters["status"] = status
    if driver_id:
        filters["driver_id"] = driver_id
    
    trip_service = TripService(db)
    return trip_service.get_trips(page, size, sort_by, sort_order, filters)


@router.get("/my-trips", response_model=TripListResponse)
def get_my_trips(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(all_roles)
):
    trip_service = TripService(db)
    return trip_service.get_my_trips(current_user.id, page, size)


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trip_service = TripService(db)
    return trip_service.get_trip_by_id(trip_id)


@router.post("/", response_model=TripResponse, status_code=201)
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trip_service = TripService(db)
    return trip_service.create_trip(trip_data, current_user)


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    update_data: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trip_service = TripService(db)
    return trip_service.update_trip(trip_id, update_data, current_user)


@router.delete("/{trip_id}", status_code=204)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trip_service = TripService(db)
    trip_service.delete_trip(trip_id, current_user)
    return None