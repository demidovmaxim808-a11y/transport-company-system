from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.trailer import Trailer, TrailerStatus
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class TrailerRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, trailer_id: int) -> Optional[Trailer]:
        return self.db.query(Trailer).filter(Trailer.id == trailer_id).first()
    
    def get_by_plate(self, plate_number: str) -> Optional[Trailer]:
        return self.db.query(Trailer).filter(Trailer.plate_number == plate_number).first()
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[Trailer]:
        query = self.db.query(Trailer)
        
        if filters:
            query = apply_filters(query, Trailer, filters)
        
        total = query.count()
        
        query = apply_sorting(query, Trailer, sort_by, sort_order)
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)
    
    def get_available_trailers(self) -> List[Trailer]:
        return self.db.query(Trailer).filter(
            Trailer.status == TrailerStatus.AVAILABLE
        ).all()
    
    def create(self, trailer_data: dict) -> Trailer:
        trailer = Trailer(**trailer_data)
        self.db.add(trailer)
        self.db.commit()
        self.db.refresh(trailer)
        return trailer
    
    def update(self, trailer: Trailer, update_data: dict) -> Trailer:
        for key, value in update_data.items():
            if hasattr(trailer, key) and value is not None:
                setattr(trailer, key, value)
        
        self.db.commit()
        self.db.refresh(trailer)
        return trailer
    
    def delete(self, trailer: Trailer) -> None:
        self.db.delete(trailer)
        self.db.commit()