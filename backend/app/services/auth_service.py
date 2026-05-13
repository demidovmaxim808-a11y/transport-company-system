from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.audit_repository import AuditRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import BadRequestException, UnauthorizedException, ConflictException
from app.core.logger import logger
from app.utils.validators import validate_email, validate_password_strength
from app.schemas.auth import UserRegister, UserLogin, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def register(self, user_data: UserRegister) -> TokenResponse:
        if not validate_email(user_data.email):
            raise BadRequestException("Invalid email format")
        
        is_valid, msg = validate_password_strength(user_data.password)
        if not is_valid:
            raise BadRequestException(msg)
        
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ConflictException("User with this email already exists")
        
        hashed_password = hash_password(user_data.password)
        
        user = self.user_repo.create({
            "email": user_data.email,
            "password_hash": hashed_password,
            "full_name": user_data.full_name,
            "role": "driver"
        })
        
        self.audit_repo.create_log(
            user_id=user.id,
            action="REGISTER",
            entity_name="User",
            entity_id=user.id,
            details=f"User {user.email} registered"
        )
        
        logger.info(f"New user registered: {user.email}")
        
        return self._generate_token_response(user)
    
    def login(self, login_data: UserLogin) -> TokenResponse:
        user = self.user_repo.get_by_email(login_data.email)
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        self.audit_repo.create_log(
            user_id=user.id,
            action="LOGIN",
            entity_name="User",
            entity_id=user.id,
            details=f"User {user.email} logged in"
        )
        
        logger.info(f"User logged in: {user.email}")
        
        return self._generate_token_response(user)
    
    def _generate_token_response(self, user: User) -> TokenResponse:
        access_token = create_access_token({
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else user.role
        })
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            role=user.role.value if hasattr(user.role, 'value') else user.role,
            full_name=user.full_name
        )