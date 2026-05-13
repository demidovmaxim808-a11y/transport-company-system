from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


class RevenueByPeriod(BaseModel):
    period: str
    revenue: float
    orders_count: int


class DriverPerformance(BaseModel):
    driver_id: int
    driver_name: str
    trips_count: int
    total_km: float
    revenue_generated: float


class TrailerUtilization(BaseModel):
    trailer_id: int
    plate_number: str
    trips_count: int
    utilization_percent: float


class OrderStatusSummary(BaseModel):
    status: str
    count: int
    percentage: float


class DashboardAnalytics(BaseModel):
    total_revenue: float
    total_orders: int
    active_trips: int
    available_drivers: int
    available_trailers: int
    revenue_by_month: List[RevenueByPeriod]
    top_drivers: List[DriverPerformance]
    trailer_utilization: List[TrailerUtilization]
    order_status_summary: List[OrderStatusSummary]