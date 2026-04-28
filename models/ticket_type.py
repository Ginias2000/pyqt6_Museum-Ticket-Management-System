"""
Ticket Type Data Model
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class TicketType:
    """Ticket type data model"""
    id: Optional[int] = None
    name: str = ""
    price: float = 0.0
    description: str = ""
    is_active: bool = True
    created_at: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(**data)