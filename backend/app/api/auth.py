from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register(user_data)


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login(login_data)