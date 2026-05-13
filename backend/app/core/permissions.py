from fastapi import Depends, HTTPException, status
from typing import List
from functools import wraps

from app.models.user import User
from app.core.security import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' not allowed. Required roles: {self.allowed_roles}"
            )
        return current_user


admin_only = RoleChecker(["admin"])
admin_or_manager = RoleChecker(["admin", "manager"])
manager_only = RoleChecker(["manager"])
driver_only = RoleChecker(["driver"])
all_roles = RoleChecker(["admin", "manager", "driver"])