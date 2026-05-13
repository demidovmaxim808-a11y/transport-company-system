from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager
from app.models.user import User
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse, DriverListResponse
from app.services.driver_service import DriverService

router = APIRouter(prefix="/api/drivers", tags=["drivers"])


@router.get("/", response_model=DriverListResponse)
def get_drivers(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    filters = {}
    if status:
        filters["status"] = status
    
    driver_service = DriverService(db)
    return driver_service.get_drivers(page, size, sort_by, sort_order, filters)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    driver_service = DriverService(db)
    return driver_service.get_driver_by_id(driver_id)


@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(
    driver_data: DriverCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    driver_service = DriverService(db)
    return driver_service.create_driver(driver_data, current_user)


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    update_data: DriverUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    driver_service = DriverService(db)
    return driver_service.update_driver(driver_id, update_data, current_user)


@router.delete("/{driver_id}", status_code=204)
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    driver_service = DriverService(db)
    driver_service.delete_driver(driver_id, current_user)
    return None