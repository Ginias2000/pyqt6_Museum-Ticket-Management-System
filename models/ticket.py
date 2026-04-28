"""
Ticket Data Model
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Ticket:
    """Ticket data model"""
    id: Optional[int] = None
    ticket_id: str = ""
    visitor_id: int = None
    ticket_type_id: int = None
    price: float = 0.0
    sale_time: str = ""
    status: str = "purchased"  # purchased, visiting, used, expired, cancelled, left
    remaining_uses: int = 1
    created_at: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(**data)