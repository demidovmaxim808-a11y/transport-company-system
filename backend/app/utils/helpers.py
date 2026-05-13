from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import desc, asc
from sqlalchemy.orm import Query


def apply_filters(query: Query, model: Any, filters: Dict[str, Any]) -> Query:
    for field, value in filters.items():
        if value is not None and hasattr(model, field):
            query = query.filter(getattr(model, field) == value)
    return query


def apply_sorting(query: Query, model: Any, sort_by: Optional[str], sort_order: Optional[str]) -> Query:
    if sort_by and hasattr(model, sort_by):
        order_func = desc if sort_order == "desc" else asc
        query = query.order_by(order_func(getattr(model, sort_by)))
    return query


def apply_pagination(query: Query, page: int = 1, size: int = 20) -> Query:
    if page < 1:
        page = 1
    if size < 1:
        size = 20
    if size > 100:
        size = 100
    
    offset = (page - 1) * size
    return query.offset(offset).limit(size)


def get_date_range(period: str) -> tuple:
    end_date = datetime.utcnow()
    
    if period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "quarter":
        start_date = end_date - timedelta(days=90)
    elif period == "year":
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    
    return start_date, end_date