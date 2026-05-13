import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.models.user import User, UserRole

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    admin_user = User(
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        full_name="Admin Test"
    )
    db.add(admin_user)
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_register_user(test_db):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "user123",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "newuser@test.com"
    assert data["role"] == "driver"


def test_register_duplicate_user(test_db):
    client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "user123",
            "full_name": "Duplicate User"
        }
    )
    
    response = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@test.com",
            "password": "user123",
            "full_name": "Duplicate User 2"
        }
    )
    
    assert response.status_code == 409


def test_login_success(test_db):
    client.post(
        "/api/auth/register",
        json={
            "email": "logintest@test.com",
            "password": "login123",
            "full_name": "Login Test"
        }
    )
    
    response = client.post(
        "/api/auth/login",
        json={
            "email": "logintest@test.com",
            "password": "login123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(test_db):
    client.post(
        "/api/auth/register",
        json={
            "email": "wrong@test.com",
            "password": "correct123",
            "full_name": "Wrong Pass"
        }
    )
    
    response = client.post(
        "/api/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401