from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_log import AuditLogResponse, AuditLogListResponse


class AuditService:
    def __init__(self, db: Session):
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_audit_logs(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc",
        filters: Optional[Dict[str, Any]] = None
    ) -> AuditLogListResponse:
        result = self.audit_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return AuditLogListResponse(
            items=[AuditLogResponse.model_validate(log) for log in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )