from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_only
from app.models.user import User
from app.schemas.audit_log import AuditLogListResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/api/audit-logs", tags=["audit-logs"])


@router.get("/", response_model=AuditLogListResponse)
def get_audit_logs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc"),
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    filters = {}
    if user_id:
        filters["user_id"] = user_id
    if action:
        filters["action"] = action
    
    audit_service = AuditService(db)
    return audit_service.get_audit_logs(page, size, sort_by, sort_order, filters)