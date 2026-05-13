from sqlalchemy.orm import Session
from app.models.trailer import Trailer, TrailerStatus


def seed_trailers(db: Session):
    trailers = [
        {
            "model": "Volvo FH16",
            "plate_number": "TR-001-AAA",
            "capacity": 25000.0,
            "status": TrailerStatus.AVAILABLE
        },
        {
            "model": "Scania R730",
            "plate_number": "TR-002-BBB",
            "capacity": 28000.0,
            "status": TrailerStatus.IN_USE
        },
        {
            "model": "MAN TGX",
            "plate_number": "TR-003-CCC",
            "capacity": 24000.0,
            "status": TrailerStatus.AVAILABLE
        },
        {
            "model": "Mercedes Actros",
            "plate_number": "TR-004-DDD",
            "capacity": 26000.0,
            "status": TrailerStatus.MAINTENANCE
        }
    ]
    
    for trailer_data in trailers:
        existing = db.query(Trailer).filter(Trailer.plate_number == trailer_data["plate_number"]).first()
        if not existing:
            trailer = Trailer(**trailer_data)
            db.add(trailer)
    
    db.commit()
    print("Trailers seeded successfully")