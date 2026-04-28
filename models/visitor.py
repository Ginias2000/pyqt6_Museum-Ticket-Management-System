"""
Visitor Data Model
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Visitor:
    """Visitor data model"""
    id: Optional[int] = None
    id_number: str = ""
    name: str = ""
    gender: str = ""
    date_of_birth: str = ""
    phone: str = ""
    email: str = ""
    created_at: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(**data)