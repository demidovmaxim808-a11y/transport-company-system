from typing import Optional
from sqlalchemy.orm import Session

from app.models.route import Route
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class RouteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, route_id: int) -> Optional[Route]:
        return self.db.query(Route).filter(Route.id == route_id).first()
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[Route]:
        query = self.db.query(Route)
        
        if filters:
            query = apply_filters(query, Route, filters)
        
        total = query.count()
        
        query = apply_sorting(query, Route, sort_by, sort_order)
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)
    
    def create(self, route_data: dict) -> Route:
        route = Route(**route_data)
        self.db.add(route)
        self.db.commit()
        self.db.refresh(route)
        return route
    
    def update(self, route: Route, update_data: dict) -> Route:
        for key, value in update_data.items():
            if hasattr(route, key) and value is not None:
                setattr(route, key, value)
        
        self.db.commit()
        self.db.refresh(route)
        return route
    
    def delete(self, route: Route) -> None:
        self.db.delete(route)
        self.db.commit()