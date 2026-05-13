import re
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    pattern = r'^\+?[\d\s\-\(\)]{7,20}$'
    return bool(re.match(pattern, phone))


def validate_plate_number(plate: str) -> bool:
    pattern = r'^[A-Z0-9]{5,20}$'
    return bool(re.match(pattern, plate.upper()))


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 128:
        return False, "Password must not exceed 128 characters"
    
    if not re.search(r'[A-Z]', password) and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None