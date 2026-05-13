from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import admin_or_manager
from app.models.user import User
from app.schemas.analytics import DashboardAnalytics
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardAnalytics)
def get_dashboard_analytics(
    period: str = Query("month", regex="^(week|month|quarter|year)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_or_manager)
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_dashboard_analytics(period)