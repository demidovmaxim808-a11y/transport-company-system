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
        full_name="Admin Test"
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    global admin_token
    admin_token = create_access_token({
        "user_id": admin_user.id,
        "email": admin_user.email,
        "role": admin_user.role.value
    })
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_order(test_db):
    response = client.post(
        "/api/orders/",
        json={
            "customer_name": "Test Customer",
            "cargo_type": "Test Cargo",
            "cargo_weight": 1000.0,
            "trip_id": None,
            "status": "pending",
            "price": 5000.0
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["cargo_type"] == "Test Cargo"
    assert data["cargo_weight"] == 1000.0


def test_get_orders(test_db):
    client.post(
        "/api/orders/",
        json={
            "customer_name": "Customer 1",
            "cargo_type": "Electronics",
            "cargo_weight": 2000.0,
            "trip_id": None,
            "status": "pending",
            "price": 8000.0
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get(
        "/api/orders/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert len(data["items"]) > 0


def test_update_order_status(test_db):
    create_response = client.post(
        "/api/orders/",
        json={
            "customer_name": "Customer Update",
            "cargo_type": "Food",
            "cargo_weight": 1500.0,
            "trip_id": None,
            "status": "pending",
            "price": 6000.0
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    order_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/orders/{order_id}",
        json={"status": "in_transit"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "in_transit"