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
    manager_user = User(
        email="manager@test.com",
        password_hash=hash_password("manager123"),
        role=UserRole.MANAGER,
        full_name="Manager Test"
    )
    db.add(admin_user)
    db.add(manager_user)
    db.commit()
    db.refresh(admin_user)
    db.refresh(manager_user)
    
    global admin_token, manager_token
    admin_token = create_access_token({
        "user_id": admin_user.id,
        "email": admin_user.email,
        "role": admin_user.role.value
    })
    manager_token = create_access_token({
        "user_id": manager_user.id,
        "email": manager_user.email,
        "role": manager_user.role.value
    })
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_driver(test_db):
    response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Test Driver",
            "license_number": "DL-TEST-001",
            "phone": "+1-555-9999",
            "experience_years": 4.5,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Test Driver"
    assert data["license_number"] == "DL-TEST-001"
    assert data["phone"] == "+1-555-9999"
    assert data["experience_years"] == 4.5
    assert data["status"] == "available"


def test_create_driver_duplicate_license(test_db):
    client.post(
        "/api/drivers/",
        json={
            "full_name": "First Driver",
            "license_number": "DL-DUP-001",
            "phone": "+1-555-1111",
            "experience_years": 2.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Second Driver",
            "license_number": "DL-DUP-001",
            "phone": "+1-555-2222",
            "experience_years": 3.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_get_drivers(test_db):
    client.post(
        "/api/drivers/",
        json={
            "full_name": "Driver One",
            "license_number": "DL-LIST-001",
            "phone": "+1-555-3333",
            "experience_years": 5.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    client.post(
        "/api/drivers/",
        json={
            "full_name": "Driver Two",
            "license_number": "DL-LIST-002",
            "phone": "+1-555-4444",
            "experience_years": 3.0,
            "status": "busy"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get(
        "/api/drivers/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2


def test_get_drivers_with_filters(test_db):
    client.post(
        "/api/drivers/",
        json={
            "full_name": "Available Driver",
            "license_number": "DL-FILT-001",
            "phone": "+1-555-5555",
            "experience_years": 6.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    client.post(
        "/api/drivers/",
        json={
            "full_name": "Busy Driver",
            "license_number": "DL-FILT-002",
            "phone": "+1-555-6666",
            "experience_years": 4.0,
            "status": "busy"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get(
        "/api/drivers/?status=available",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    for driver in data["items"]:
        assert driver["status"] == "available"


def test_get_driver_by_id(test_db):
    create_response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Get By ID Driver",
            "license_number": "DL-GET-001",
            "phone": "+1-555-7777",
            "experience_years": 7.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    driver_id = create_response.json()["id"]
    
    response = client.get(
        f"/api/drivers/{driver_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == driver_id
    assert data["full_name"] == "Get By ID Driver"
    assert data["license_number"] == "DL-GET-001"


def test_get_driver_not_found(test_db):
    response = client.get(
        "/api/drivers/99999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 404


def test_update_driver(test_db):
    create_response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Update Driver",
            "license_number": "DL-UPD-001",
            "phone": "+1-555-8888",
            "experience_years": 3.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    driver_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/drivers/{driver_id}",
        json={
            "full_name": "Updated Driver Name",
            "experience_years": 5.0,
            "status": "busy"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Driver Name"
    assert data["experience_years"] == 5.0
    assert data["status"] == "busy"
    assert data["phone"] == "+1-555-8888"


def test_update_driver_partial(test_db):
    create_response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Partial Update",
            "license_number": "DL-PART-001",
            "phone": "+1-555-9999",
            "experience_years": 2.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    driver_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/drivers/{driver_id}",
        json={
            "status": "off_duty"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "off_duty"
    assert data["full_name"] == "Partial Update"


def test_delete_driver(test_db):
    create_response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Delete Driver",
            "license_number": "DL-DEL-001",
            "phone": "+1-555-0000",
            "experience_years": 1.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    driver_id = create_response.json()["id"]
    
    response = client.delete(
        f"/api/drivers/{driver_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get(
        f"/api/drivers/{driver_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert get_response.status_code == 404


def test_manager_can_manage_drivers(test_db):
    response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Manager Created Driver",
            "license_number": "DL-MGR-001",
            "phone": "+1-555-1212",
            "experience_years": 3.5,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    
    assert response.status_code == 201
    
    response = client.get(
        "/api/drivers/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    
    assert response.status_code == 200


def test_invalid_phone_format(test_db):
    response = client.post(
        "/api/drivers/",
        json={
            "full_name": "Invalid Phone",
            "license_number": "DL-PH-001",
            "phone": "123",
            "experience_years": 1.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code in [400, 422]


def test_pagination(test_db):
    for i in range(5):
        client.post(
            "/api/drivers/",
            json={
                "full_name": f"Pagination Driver {i}",
                "license_number": f"DL-PAG-{i:03d}",
                "phone": f"+1-555-1{i:04d}",
                "experience_years": float(i + 1),
                "status": "available"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    response = client.get(
        "/api/drivers/?page=1&size=2",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 2
    assert data["page"] == 1
    assert data["size"] == 2