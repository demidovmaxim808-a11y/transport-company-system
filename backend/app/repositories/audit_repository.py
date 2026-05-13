from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.audit_log import AuditLog
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_log(
        self,
        user_id: int,
        action: str,
        entity_name: str,
        entity_id: Optional[int] = None,
        details: Optional[str] = None
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            details=details,
            created_at=datetime.utcnow()
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "desc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[AuditLog]:
        query = self.db.query(AuditLog)
        
        if filters:
            query = apply_filters(query, AuditLog, filters)
        
        total = query.count()
        
        query = apply_sorting(query, AuditLog, sort_by or "created_at", sort_order or "desc")
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)