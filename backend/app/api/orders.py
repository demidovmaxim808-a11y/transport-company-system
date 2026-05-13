from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager, all_roles
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/", response_model=OrderListResponse)
def get_orders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(all_roles)
):
    filters = {}
    if status:
        filters["status"] = status
    
    order_service = OrderService(db)
    return order_service.get_orders(page, size, sort_by, sort_order, filters)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(all_roles)
):
    order_service = OrderService(db)
    return order_service.get_order_by_id(order_id)


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    order_service = OrderService(db)
    return order_service.create_order(order_data, current_user)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    order_service = OrderService(db)
    return order_service.update_order(order_id, update_data, current_user)


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    order_service = OrderService(db)
    order_service.delete_order(order_id, current_user)
    return None