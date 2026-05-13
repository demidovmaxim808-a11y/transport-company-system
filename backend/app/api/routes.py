from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager
from app.models.user import User
from app.schemas.route import RouteCreate, RouteUpdate, RouteResponse, RouteListResponse
from app.services.route_service import RouteService

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.get("/", response_model=RouteListResponse)
def get_routes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    route_service = RouteService(db)
    return route_service.get_routes(page, size, sort_by, sort_order)


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    route_service = RouteService(db)
    return route_service.get_route_by_id(route_id)


@router.post("/", response_model=RouteResponse, status_code=201)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    route_service = RouteService(db)
    return route_service.create_route(route_data, current_user)


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(
    route_id: int,
    update_data: RouteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    route_service = RouteService(db)
    return route_service.update_route(route_id, update_data, current_user)


@router.delete("/{route_id}", status_code=204)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    route_service = RouteService(db)
    route_service.delete_route(route_id, current_user)
    return None