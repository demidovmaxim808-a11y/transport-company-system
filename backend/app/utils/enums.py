from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    DRIVER = "driver"


class DriverStatusEnum(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFF_DUTY = "off_duty"
    ON_LEAVE = "on_leave"


class TrailerStatusEnum(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"


class TripStatusEnum(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"