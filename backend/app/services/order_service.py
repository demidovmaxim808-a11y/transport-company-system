from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException
from app.core.logger import logger
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse


class OrderService:
    def __init__(self, db: Session):
        self.order_repo = OrderRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_orders(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> OrderListResponse:
        result = self.order_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return OrderListResponse(
            items=[OrderResponse.model_validate(order) for order in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        return OrderResponse.model_validate(order)
    
    def create_order(self, order_data: OrderCreate, current_user: User) -> OrderResponse:
        order = self.order_repo.create(order_data.model_dump())
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="CREATE",
            entity_name="Order",
            entity_id=order.id,
            details=f"Order created for customer {order.customer_name}"
        )
        
        logger.info(f"Order created: ID {order.id}")
        
        return OrderResponse.model_validate(order)
    
    def update_order(self, order_id: int, update_data: OrderUpdate, current_user: User) -> OrderResponse:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_order = self.order_repo.update(order, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="Order",
            entity_id=order_id,
            details=f"Order updated"
        )
        
        logger.info(f"Order updated: ID {order_id}")
        
        return OrderResponse.model_validate(updated_order)
    
    def delete_order(self, order_id: int, current_user: User) -> None:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        
        self.order_repo.delete(order)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="Order",
            entity_id=order_id,
            details=f"Order deleted"
        )
        
        logger.info(f"Order deleted: ID {order_id}")