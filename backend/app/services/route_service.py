from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.route_repository import RouteRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException
from app.core.logger import logger
from app.schemas.route import RouteCreate, RouteUpdate, RouteResponse, RouteListResponse


class RouteService:
    def __init__(self, db: Session):
        self.route_repo = RouteRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_routes(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> RouteListResponse:
        result = self.route_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return RouteListResponse(
            items=[RouteResponse.model_validate(route) for route in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_route_by_id(self, route_id: int) -> RouteResponse:
        route = self.route_repo.get_by_id(route_id)
        if not route:
            raise NotFoundException("Route not found")
        return RouteResponse.model_validate(route)
    
    def create_route(self, route_data: RouteCreate, current_user: User) -> RouteResponse:
        route = self.route_repo.create(route_data.model_dump())
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="CREATE",
            entity_name="Route",
            entity_id=route.id,
            details=f"Route from {route.departure_point} to {route.destination_point} created"
        )
        
        logger.info(f"Route created: {route.departure_point} -> {route.destination_point}")
        
        return RouteResponse.model_validate(route)
    
    def update_route(self, route_id: int, update_data: RouteUpdate, current_user: User) -> RouteResponse:
        route = self.route_repo.get_by_id(route_id)
        if not route:
            raise NotFoundException("Route not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_route = self.route_repo.update(route, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="Route",
            entity_id=route_id,
            details=f"Route updated"
        )
        
        logger.info(f"Route updated: ID {route_id}")
        
        return RouteResponse.model_validate(updated_route)
    
    def delete_route(self, route_id: int, current_user: User) -> None:
        route = self.route_repo.get_by_id(route_id)
        if not route:
            raise NotFoundException("Route not found")
        
        self.route_repo.delete(route)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="Route",
            entity_id=route_id,
            details=f"Route deleted"
        )
        
        logger.info(f"Route deleted: ID {route_id}")