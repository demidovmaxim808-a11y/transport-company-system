from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager
from app.models.user import User
from app.schemas.trailer import TrailerCreate, TrailerUpdate, TrailerResponse, TrailerListResponse
from app.services.trailer_service import TrailerService

router = APIRouter(prefix="/api/trailers", tags=["trailers"])


@router.get("/", response_model=TrailerListResponse)
def get_trailers(
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
    
    trailer_service = TrailerService(db)
    return trailer_service.get_trailers(page, size, sort_by, sort_order, filters)


@router.get("/{trailer_id}", response_model=TrailerResponse)
def get_trailer(
    trailer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trailer_service = TrailerService(db)
    return trailer_service.get_trailer_by_id(trailer_id)


@router.post("/", response_model=TrailerResponse, status_code=201)
def create_trailer(
    trailer_data: TrailerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trailer_service = TrailerService(db)
    return trailer_service.create_trailer(trailer_data, current_user)


@router.put("/{trailer_id}", response_model=TrailerResponse)
def update_trailer(
    trailer_id: int,
    update_data: TrailerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trailer_service = TrailerService(db)
    return trailer_service.update_trailer(trailer_id, update_data, current_user)


@router.delete("/{trailer_id}", status_code=204)
def delete_trailer(
    trailer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    trailer_service = TrailerService(db)
    trailer_service.delete_trailer(trailer_id, current_user)
    return None