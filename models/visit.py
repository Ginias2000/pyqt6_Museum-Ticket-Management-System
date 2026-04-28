"""
Visit Data Model
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Visit:
    """Visit tracking data model"""
    id: Optional[int] = None
    ticket_id: int = None
    entry_time: str = ""
    exit_time: Optional[str] = None
    created_at: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(**data)