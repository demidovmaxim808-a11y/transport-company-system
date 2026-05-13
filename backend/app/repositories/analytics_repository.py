from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta

from app.models.order import Order, OrderStatus
from app.models.trip import Trip, TripStatus
from app.models.driver import Driver, DriverStatus
from app.models.trailer import Trailer, TrailerStatus
from app.models.route import Route


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_total_revenue(self, start_date: datetime = None, end_date: datetime = None) -> float:
        query = self.db.query(func.coalesce(func.sum(Order.price), 0))
        
        if start_date and end_date:
            query = query.filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )
        
        return query.scalar()
    
    def get_total_orders_count(self, start_date: datetime = None, end_date: datetime = None) -> int:
        query = self.db.query(func.count(Order.id))
        
        if start_date and end_date:
            query = query.filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )
        
        return query.scalar()
    
    def get_active_trips_count(self) -> int:
        return self.db.query(func.count(Trip.id)).filter(
            Trip.status == TripStatus.IN_PROGRESS
        ).scalar()
    
    def get_available_drivers_count(self) -> int:
        return self.db.query(func.count(Driver.id)).filter(
            Driver.status == DriverStatus.AVAILABLE
        ).scalar()
    
    def get_available_trailers_count(self) -> int:
        return self.db.query(func.count(Trailer.id)).filter(
            Trailer.status == TrailerStatus.AVAILABLE
        ).scalar()
    
    def get_revenue_by_month(self, months: int = 12) -> List[Dict[str, Any]]:
        current_date = datetime.utcnow()
        start_date = current_date - timedelta(days=30 * months)
        
        results = []
        for i in range(months):
            month_start = start_date + timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            
            revenue = self.db.query(func.coalesce(func.sum(Order.price), 0)).filter(
                Order.created_at >= month_start,
                Order.created_at < month_end
            ).scalar()
            
            orders_count = self.db.query(func.count(Order.id)).filter(
                Order.created_at >= month_start,
                Order.created_at < month_end
            ).scalar()
            
            results.append({
                "period": month_start.strftime("%Y-%m"),
                "revenue": revenue,
                "orders_count": orders_count
            })
        
        return results
    
    def get_top_drivers(self, limit: int = 5, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        query = self.db.query(
            Driver.id,
            Driver.full_name,
            func.count(Trip.id).label('trips_count'),
            func.coalesce(func.sum(Route.distance_km), 0).label('total_km'),
            func.coalesce(func.sum(Order.price), 0).label('revenue_generated')
        ).join(Trip, Trip.driver_id == Driver.id
        ).join(Route, Route.id == Trip.route_id
        ).outerjoin(Order, Order.trip_id == Trip.id)
        
        if start_date and end_date:
            query = query.filter(
                Trip.created_at >= start_date,
                Trip.created_at <= end_date
            )
        
        query = query.group_by(Driver.id, Driver.full_name)
        query = query.order_by(func.sum(Order.price).desc())
        query = query.limit(limit)
        
        results = query.all()
        
        return [
            {
                "driver_id": r[0],
                "driver_name": r[1],
                "trips_count": r[2],
                "total_km": float(r[3]),
                "revenue_generated": float(r[4])
            }
            for r in results
        ]
    
    def get_trailer_utilization(self, start_date: datetime = None, end_date: datetime = None) -> List[Dict[str, Any]]:
        total_trailers = self.db.query(func.count(Trailer.id)).scalar()
        
        if total_trailers == 0:
            return []
        
        query = self.db.query(
            Trailer.id,
            Trailer.plate_number,
            func.count(Trip.id).label('trips_count')
        ).outerjoin(Trip, Trip.trailer_id == Trailer.id)
        
        if start_date and end_date:
            query = query.filter(
                Trip.created_at >= start_date,
                Trip.created_at <= end_date
            )
        
        query = query.group_by(Trailer.id, Trailer.plate_number)
        results = query.all()
        
        return [
            {
                "trailer_id": r[0],
                "plate_number": r[1],
                "trips_count": r[2],
                "utilization_percent": round((r[2] / max(total_trailers, 1)) * 100, 2)
            }
            for r in results
        ]
    
    def get_order_status_summary(self) -> List[Dict[str, Any]]:
        total_orders = self.db.query(func.count(Order.id)).scalar()
        
        if total_orders == 0:
            return []
        
        query = self.db.query(
            Order.status,
            func.count(Order.id)
        ).group_by(Order.status)
        
        results = query.all()
        
        return [
            {
                "status": r[0].value,
                "count": r[1],
                "percentage": round((r[1] / total_orders) * 100, 2)
            }
            for r in results
        ]