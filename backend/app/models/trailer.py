from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TrailerStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"


class Trailer(Base):
    __tablename__ = "trailers"
    
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(150), nullable=False)
    plate_number = Column(String(20), unique=True, nullable=False)
    capacity = Column(Float, nullable=False)
    status = Column(Enum(TrailerStatus), default=TrailerStatus.AVAILABLE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    trips = relationship("Trip", back_populates="trailer")