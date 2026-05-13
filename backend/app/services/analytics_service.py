from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import DashboardAnalytics
from app.utils.helpers import get_date_range


class AnalyticsService:
    def __init__(self, db: Session):
        self.analytics_repo = AnalyticsRepository(db)
        self.db = db
    
    def get_dashboard_analytics(self, period: str = "month") -> DashboardAnalytics:
        start_date, end_date = get_date_range(period)
        
        total_revenue = self.analytics_repo.get_total_revenue(start_date, end_date)
        total_orders = self.analytics_repo.get_total_orders_count(start_date, end_date)
        active_trips = self.analytics_repo.get_active_trips_count()
        available_drivers = self.analytics_repo.get_available_drivers_count()
        available_trailers = self.analytics_repo.get_available_trailers_count()
        
        revenue_by_month = self.analytics_repo.get_revenue_by_month()
        top_drivers = self.analytics_repo.get_top_drivers(5, start_date, end_date)
        trailer_utilization = self.analytics_repo.get_trailer_utilization(start_date, end_date)
        order_status_summary = self.analytics_repo.get_order_status_summary()
        
        return DashboardAnalytics(
            total_revenue=total_revenue,
            total_orders=total_orders,
            active_trips=active_trips,
            available_drivers=available_drivers,
            available_trailers=available_trailers,
            revenue_by_month=revenue_by_month,
            top_drivers=top_drivers,
            trailer_utilization=trailer_utilization,
            order_status_summary=order_status_summary
        )