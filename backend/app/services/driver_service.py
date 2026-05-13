from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.driver_repository import DriverRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logger import logger
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse, DriverListResponse
from app.utils.validators import validate_phone


class DriverService:
    def __init__(self, db: Session):
        self.driver_repo = DriverRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_drivers(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> DriverListResponse:
        result = self.driver_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return DriverListResponse(
            items=[DriverResponse.model_validate(driver) for driver in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_driver_by_id(self, driver_id: int) -> DriverResponse:
        driver = self.driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundException("Driver not found")
        return DriverResponse.model_validate(driver)
    
    def create_driver(self, driver_data: DriverCreate, current_user: User) -> DriverResponse:
        if not validate_phone(driver_data.phone):
            raise BadRequestException("Invalid phone number format")
        
        existing = self.driver_repo.get_by_license(driver_data.license_number)
        if existing:
            raise BadRequestException("Driver with this license number already exists")
        
        driver = self.driver_repo.create(driver_data.model_dump())
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="CREATE",
            entity_name="Driver",
            entity_id=driver.id,
            details=f"Driver {driver.full_name} created"
        )
        
        logger.info(f"Driver created: {driver.full_name}")
        
        return DriverResponse.model_validate(driver)
    
    def update_driver(self, driver_id: int, update_data: DriverUpdate, current_user: User) -> DriverResponse:
        driver = self.driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundException("Driver not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_driver = self.driver_repo.update(driver, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="Driver",
            entity_id=driver_id,
            details=f"Driver {updated_driver.full_name} updated"
        )
        
        logger.info(f"Driver updated: {updated_driver.full_name}")
        
        return DriverResponse.model_validate(updated_driver)
    
    def delete_driver(self, driver_id: int, current_user: User) -> None:
        driver = self.driver_repo.get_by_id(driver_id)
        if not driver:
            raise NotFoundException("Driver not found")
        
        self.driver_repo.delete(driver)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="Driver",
            entity_id=driver_id,
            details=f"Driver {driver.full_name} deleted"
        )
        
        logger.info(f"Driver deleted: {driver.full_name}")