import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User, UserRole

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
        full_name="Admin"
    )
    driver_user = User(
        email="driver@test.com",
        password_hash=hash_password("driver123"),
        role=UserRole.DRIVER,
        full_name="Driver"
    )
    db.add(admin_user)
    db.add(driver_user)
    db.commit()
    db.refresh(admin_user)
    db.refresh(driver_user)
    
    global admin_token, driver_token
    admin_token = create_access_token({
        "user_id": admin_user.id,
        "email": admin_user.email,
        "role": admin_user.role.value
    })
    driver_token = create_access_token({
        "user_id": driver_user.id,
        "email": driver_user.email,
        "role": driver_user.role.value
    })
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_driver_cannot_access_admin_routes(test_db):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {driver_token}"}
    )
    
    assert response.status_code == 403


def test_admin_can_access_all_routes(test_db):
    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200