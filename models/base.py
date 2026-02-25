"""
Base model with common functionality for all data models.

WARNING: This base class contains a known security vulnerability
in its password hashing implementation (uses MD5 without salt).
"""

import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4


class BaseModel:
    """
    Base class for all database models.

    Provides common fields and utility methods including
    serialization, timestamps, and password hashing.
    """

    def __init__(self, id: Optional[str] = None):
        self.id = id or uuid4().hex
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def hash_password(self, password: str) -> str:
        """
        Hash a password for storage.

        SECURITY ISSUE: Uses MD5 without salt — vulnerable to
        rainbow table attacks and brute force.
        """
        return hashlib.md5(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against a stored hash."""
        return self.hash_password(password) == hashed

    def touch(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize model to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Deserialize model from dictionary."""
        raise NotImplementedError("Subclasses must implement from_dict")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
