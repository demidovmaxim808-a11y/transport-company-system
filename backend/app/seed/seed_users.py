from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.security import hash_password


def seed_users(db: Session):
    users = [
        {
            "email": "admin@transport.com",
            "password_hash": hash_password("admin123"),
            "role": UserRole.ADMIN,
            "full_name": "Admin User"
        },
        {
            "email": "manager@transport.com",
            "password_hash": hash_password("manager123"),
            "role": UserRole.MANAGER,
            "full_name": "Manager User"
        },
        {
            "email": "driver1@transport.com",
            "password_hash": hash_password("driver123"),
            "role": UserRole.DRIVER,
            "full_name": "John Driver"
        },
        {
            "email": "driver2@transport.com",
            "password_hash": hash_password("driver123"),
            "role": UserRole.DRIVER,
            "full_name": "Jane Driver"
        }
    ]
    
    for user_data in users:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing:
            user = User(**user_data)
            db.add(user)
    
    db.commit()
    print("Users seeded successfully")