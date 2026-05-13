from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logger import logger
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.utils.pagination import PaginatedResults


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_users(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> UserListResponse:
        result = self.user_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return UserListResponse(
            items=[UserResponse.model_validate(user) for user in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, update_data: UserUpdate, current_user: User) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        if update_data.role and current_user.role.value != "admin":
            raise BadRequestException("Only admin can change user roles")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_user = self.user_repo.update(user, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="User",
            entity_id=user_id,
            details=f"User {user.email} updated"
        )
        
        logger.info(f"User updated: {user.email}")
        
        return UserResponse.model_validate(updated_user)
    
    def delete_user(self, user_id: int, current_user: User) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        self.user_repo.delete(user)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="User",
            entity_id=user_id,
            details=f"User {user.email} deleted"
        )
        
        logger.info(f"User deleted: {user.email}")