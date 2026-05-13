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
    driver_user = User(
        email="driver@test.com",
        password_hash=hash_password("driver123"),
        role=UserRole.DRIVER,
        full_name="Driver Test"
    )
    db.add(admin_user)
    db.add(manager_user)
    db.add(driver_user)
    db.commit()
    db.refresh(admin_user)
    db.refresh(manager_user)
    db.refresh(driver_user)
    
    global admin_token, manager_token, driver_token
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
    driver_token = create_access_token({
        "user_id": driver_user.id,
        "email": driver_user.email,
        "role": driver_user.role.value
    })
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_trailer(test_db):
    response = client.post(
        "/api/trailers/",
        json={
            "model": "Volvo FH16",
            "plate_number": "ABC123",
            "capacity": 25000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["model"] == "Volvo FH16"
    assert data["plate_number"] == "ABC123"
    assert data["capacity"] == 25000.0
    assert data["status"] == "available"


def test_create_trailer_duplicate_plate(test_db):
    client.post(
        "/api/trailers/",
        json={
            "model": "Scania R730",
            "plate_number": "DUP456",
            "capacity": 28000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.post(
        "/api/trailers/",
        json={
            "model": "MAN TGX",
            "plate_number": "DUP456",
            "capacity": 24000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


def test_get_trailers(test_db):
    client.post(
        "/api/trailers/",
        json={
            "model": "Trailer A",
            "plate_number": "PLATE01",
            "capacity": 20000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    client.post(
        "/api/trailers/",
        json={
            "model": "Trailer B",
            "plate_number": "PLATE02",
            "capacity": 22000.0,
            "status": "in_use"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get(
        "/api/trailers/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2


def test_get_trailers_with_filters(test_db):
    client.post(
        "/api/trailers/",
        json={
            "model": "Maintenance Trailer",
            "plate_number": "MAINT01",
            "capacity": 15000.0,
            "status": "maintenance"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = client.get(
        "/api/trailers/?status=maintenance",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    for trailer in data["items"]:
        assert trailer["status"] == "maintenance"


def test_get_trailer_by_id(test_db):
    create_response = client.post(
        "/api/trailers/",
        json={
            "model": "Get By ID",
            "plate_number": "GET001",
            "capacity": 30000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    trailer_id = create_response.json()["id"]
    
    response = client.get(
        f"/api/trailers/{trailer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == trailer_id
    assert data["model"] == "Get By ID"
    assert data["plate_number"] == "GET001"


def test_get_trailer_not_found(test_db):
    response = client.get(
        "/api/trailers/99999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 404


def test_update_trailer(test_db):
    create_response = client.post(
        "/api/trailers/",
        json={
            "model": "Update Me",
            "plate_number": "UPD001",
            "capacity": 18000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    trailer_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/trailers/{trailer_id}",
        json={
            "model": "Updated Model",
            "capacity": 20000.0,
            "status": "in_use"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "Updated Model"
    assert data["capacity"] == 20000.0
    assert data["status"] == "in_use"
    assert data["plate_number"] == "UPD001"


def test_update_trailer_partial(test_db):
    create_response = client.post(
        "/api/trailers/",
        json={
            "model": "Partial Trailer",
            "plate_number": "PART001",
            "capacity": 16000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    trailer_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/trailers/{trailer_id}",
        json={
            "status": "maintenance"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "maintenance"
    assert data["model"] == "Partial Trailer"


def test_delete_trailer(test_db):
    create_response = client.post(
        "/api/trailers/",
        json={
            "model": "Delete Me",
            "plate_number": "DEL001",
            "capacity": 14000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    trailer_id = create_response.json()["id"]
    
    response = client.delete(
        f"/api/trailers/{trailer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get(
        f"/api/trailers/{trailer_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert get_response.status_code == 404


def test_manager_can_manage_trailers(test_db):
    response = client.post(
        "/api/trailers/",
        json={
            "model": "Manager Trailer",
            "plate_number": "MGR001",
            "capacity": 26000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    
    assert response.status_code == 201
    
    response = client.get(
        "/api/trailers/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    
    assert response.status_code == 200


def test_driver_cannot_manage_trailers(test_db):
    response = client.get(
        "/api/trailers/",
        headers={"Authorization": f"Bearer {driver_token}"}
    )
    
    assert response.status_code == 403


def test_invalid_plate_number_format(test_db):
    response = client.post(
        "/api/trailers/",
        json={
            "model": "Invalid Plate",
            "plate_number": "ab",
            "capacity": 10000.0,
            "status": "available"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 400


def test_pagination(test_db):
    for i in range(5):
        client.post(
            "/api/trailers/",
            json={
                "model": f"Pagination Trailer {i}",
                "plate_number": f"PAG{i:03d}",
                "capacity": float(10000 + i * 1000),
                "status": "available"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
    
    response = client.get(
        "/api/trailers/?page=1&size=2",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 2
    assert data["page"] == 1
    assert data["size"] == 2