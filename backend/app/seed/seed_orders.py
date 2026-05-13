from sqlalchemy.orm import Session
from app.models.order import Order, OrderStatus
from app.models.route import Route
from datetime import datetime


def seed_orders(db: Session):
    routes = [
        {
            "departure_point": "New York, NY",
            "destination_point": "Los Angeles, CA",
            "distance_km": 4490.0
        },
        {
            "departure_point": "Chicago, IL",
            "destination_point": "Houston, TX",
            "distance_km": 1740.0
        },
        {
            "departure_point": "Miami, FL",
            "destination_point": "Atlanta, GA",
            "distance_km": 1060.0
        }
    ]
    
    for route_data in routes:
        existing = db.query(Route).filter(
            Route.departure_point == route_data["departure_point"],
            Route.destination_point == route_data["destination_point"]
        ).first()
        if not existing:
            route = Route(**route_data)
            db.add(route)
    
    db.commit()
    
    orders = [
        {
            "customer_name": "Tech Corp",
            "cargo_type": "Electronics",
            "cargo_weight": 5000.0,
            "trip_id": None,
            "status": OrderStatus.PENDING,
            "price": 15000.0
        },
        {
            "customer_name": "Food Delivery Inc",
            "cargo_type": "Food Products",
            "cargo_weight": 8000.0,
            "trip_id": None,
            "status": OrderStatus.PENDING,
            "price": 12000.0
        },
        {
            "customer_name": "Construction Ltd",
            "cargo_type": "Building Materials",
            "cargo_weight": 15000.0,
            "trip_id": None,
            "status": OrderStatus.PENDING,
            "price": 25000.0
        }
    ]
    
    for order_data in orders:
        customer_name = order_data["customer_name"]
        existing = db.query(Order).filter(Order.customer_name == customer_name).first()
        if not existing:
            order = Order(**order_data)
            db.add(order)
    
    db.commit()
    print("Orders and Routes seeded successfully")