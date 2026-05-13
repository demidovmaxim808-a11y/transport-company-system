from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_only
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse, UserListResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=UserListResponse)
def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc"),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    filters = {}
    if role:
        filters["role"] = role
    
    user_service = UserService(db)
    return user_service.get_users(page, size, sort_by, sort_order, filters)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    user_service = UserService(db)
    return user_service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    user_service = UserService(db)
    return user_service.update_user(user_id, update_data, current_user)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    user_service = UserService(db)
    user_service.delete_user(user_id, current_user)
    return None