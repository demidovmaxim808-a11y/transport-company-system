from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.trailer_repository import TrailerRepository
from app.repositories.audit_repository import AuditRepository
from app.core.exceptions import NotFoundException, BadRequestException
from app.core.logger import logger
from app.schemas.trailer import TrailerCreate, TrailerUpdate, TrailerResponse, TrailerListResponse
from app.utils.validators import validate_plate_number


class TrailerService:
    def __init__(self, db: Session):
        self.trailer_repo = TrailerRepository(db)
        self.audit_repo = AuditRepository(db)
        self.db = db
    
    def get_trailers(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        filters: Optional[Dict[str, Any]] = None
    ) -> TrailerListResponse:
        result = self.trailer_repo.get_all(page, size, sort_by, sort_order, filters)
        
        return TrailerListResponse(
            items=[TrailerResponse.model_validate(trailer) for trailer in result.items],
            total=result.total,
            page=result.page,
            size=result.size,
            pages=result.pages
        )
    
    def get_trailer_by_id(self, trailer_id: int) -> TrailerResponse:
        trailer = self.trailer_repo.get_by_id(trailer_id)
        if not trailer:
            raise NotFoundException("Trailer not found")
        return TrailerResponse.model_validate(trailer)
    
    def create_trailer(self, trailer_data: TrailerCreate, current_user: User) -> TrailerResponse:
        if not validate_plate_number(trailer_data.plate_number):
            raise BadRequestException("Invalid plate number format")
        
        existing = self.trailer_repo.get_by_plate(trailer_data.plate_number)
        if existing:
            raise BadRequestException("Trailer with this plate number already exists")
        
        trailer = self.trailer_repo.create(trailer_data.model_dump())
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="CREATE",
            entity_name="Trailer",
            entity_id=trailer.id,
            details=f"Trailer {trailer.plate_number} created"
        )
        
        logger.info(f"Trailer created: {trailer.plate_number}")
        
        return TrailerResponse.model_validate(trailer)
    
    def update_trailer(self, trailer_id: int, update_data: TrailerUpdate, current_user: User) -> TrailerResponse:
        trailer = self.trailer_repo.get_by_id(trailer_id)
        if not trailer:
            raise NotFoundException("Trailer not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_trailer = self.trailer_repo.update(trailer, update_dict)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="UPDATE",
            entity_name="Trailer",
            entity_id=trailer_id,
            details=f"Trailer {updated_trailer.plate_number} updated"
        )
        
        logger.info(f"Trailer updated: {updated_trailer.plate_number}")
        
        return TrailerResponse.model_validate(updated_trailer)
    
    def delete_trailer(self, trailer_id: int, current_user: User) -> None:
        trailer = self.trailer_repo.get_by_id(trailer_id)
        if not trailer:
            raise NotFoundException("Trailer not found")
        
        self.trailer_repo.delete(trailer)
        
        self.audit_repo.create_log(
            user_id=current_user.id,
            action="DELETE",
            entity_name="Trailer",
            entity_id=trailer_id,
            details=f"Trailer {trailer.plate_number} deleted"
        )
        
        logger.info(f"Trailer deleted: {trailer.plate_number}")