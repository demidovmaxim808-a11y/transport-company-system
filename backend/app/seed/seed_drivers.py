from sqlalchemy.orm import Session
from app.models.driver import Driver, DriverStatus


def seed_drivers(db: Session):
    drivers = [
        {
            "full_name": "John Smith",
            "license_number": "DL-001-ABC",
            "phone": "+1-555-0101",
            "experience_years": 5.5,
            "status": DriverStatus.AVAILABLE
        },
        {
            "full_name": "Mary Johnson",
            "license_number": "DL-002-DEF",
            "phone": "+1-555-0102",
            "experience_years": 3.0,
            "status": DriverStatus.BUSY
        },
        {
            "full_name": "Robert Brown",
            "license_number": "DL-003-GHI",
            "phone": "+1-555-0103",
            "experience_years": 7.0,
            "status": DriverStatus.AVAILABLE
        },
        {
            "full_name": "Patricia Davis",
            "license_number": "DL-004-JKL",
            "phone": "+1-555-0104",
            "experience_years": 2.5,
            "status": DriverStatus.OFF_DUTY
        }
    ]
    
    for driver_data in drivers:
        existing = db.query(Driver).filter(Driver.license_number == driver_data["license_number"]).first()
        if not existing:
            driver = Driver(**driver_data)
            db.add(driver)
    
    db.commit()
    print("Drivers seeded successfully")