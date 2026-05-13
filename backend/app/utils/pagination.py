from typing import TypeVar, Generic, List
from math import ceil

T = TypeVar('T')


class PaginatedResults(Generic[T]):
    def __init__(self, items: List[T], total: int, page: int, size: int):
        self.items = items
        self.total = total
        self.page = page
        self.size = size
        self.pages = ceil(total / size) if size > 0 else 0
    
    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "size": self.size,
            "pages": self.pages
        }