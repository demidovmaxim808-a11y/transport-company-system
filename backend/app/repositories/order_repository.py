from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from app.models.order import Order, OrderStatus
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).options(
            joinedload(Order.trip)
        ).filter(Order.id == order_id).first()
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[Order]:
        query = self.db.query(Order)
        
        if filters:
            query = apply_filters(query, Order, filters)
        
        total = query.count()
        
        query = apply_sorting(query, Order, sort_by, sort_order)
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)
    
    def create(self, order_data: dict) -> Order:
        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def update(self, order: Order, update_data: dict) -> Order:
        for key, value in update_data.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()
    
    def get_orders_in_period(self, start_date: datetime, end_date: datetime) -> List[Order]:
        return self.db.query(Order).filter(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        ).all()
    
    def get_orders_by_status(self) -> dict:
        results = {}
        for status in OrderStatus:
            count = self.db.query(Order).filter(Order.status == status).count()
            results[status.value] = count
        return results