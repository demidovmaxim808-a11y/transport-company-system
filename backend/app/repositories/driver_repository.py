from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.driver import Driver, DriverStatus
from app.utils.pagination import PaginatedResults
from app.utils.helpers import apply_filters, apply_sorting, apply_pagination


class DriverRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        return self.db.query(Driver).filter(Driver.id == driver_id).first()
    
    def get_by_license(self, license_number: str) -> Optional[Driver]:
        return self.db.query(Driver).filter(Driver.license_number == license_number).first()
    
    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[dict] = None
    ) -> PaginatedResults[Driver]:
        query = self.db.query(Driver)
        
        if filters:
            query = apply_filters(query, Driver, filters)
        
        total = query.count()
        
        query = apply_sorting(query, Driver, sort_by, sort_order)
        query = apply_pagination(query, page, size)
        
        items = query.all()
        
        return PaginatedResults(items, total, page, size)
    
    def get_available_drivers(self) -> List[Driver]:
        return self.db.query(Driver).filter(
            Driver.status == DriverStatus.AVAILABLE
        ).all()
    
    def create(self, driver_data: dict) -> Driver:
        driver = Driver(**driver_data)
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver
    
    def update(self, driver: Driver, update_data: dict) -> Driver:
        for key, value in update_data.items():
            if hasattr(driver, key) and value is not None:
                setattr(driver, key, value)
        
        self.db.commit()
        self.db.refresh(driver)
        return driver
    
    def delete(self, driver: Driver) -> None:
        self.db.delete(driver)
        self.db.commit()