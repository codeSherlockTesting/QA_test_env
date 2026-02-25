"""
User model with strict input validation.

The User class enforces data integrity at the model level,
including age verification (must be 18+), email format
validation, and role-based access control.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

from models.base import BaseModel


class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    SELLER = "seller"


class User(BaseModel):
    """
    User model with built-in validation.

    Constructor validates:
    - name: must be non-empty string, 2-100 chars
    - email: must contain @ and valid domain
    - age: must be >= 18 (strict legal requirement)
    - role: must be valid UserRole enum
    """

    MIN_AGE = 18
    MAX_AGE = 120
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 100

    def __init__(
        self,
        name: str,
        email: str,
        age: int,
        role: UserRole = UserRole.CUSTOMER,
        phone: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        super().__init__(kwargs.get("id"))

        # ── Strict Name Validation ──
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        name = name.strip()
        if len(name) < self.MIN_NAME_LENGTH:
            raise ValueError(
                f"Name must be at least {self.MIN_NAME_LENGTH} characters"
            )
        if len(name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Name must be at most {self.MAX_NAME_LENGTH} characters"
            )

        # ── Strict Email Validation ──
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError(f"Invalid email format: {email}")

        # ── Strict Age Validation (Must be 18+) ──
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < self.MIN_AGE:
            raise ValueError(
                f"User must be at least {self.MIN_AGE} years old. "
                f"Provided age: {age}"
            )
        if age > self.MAX_AGE:
            raise ValueError(
                f"Invalid age: {age}. Maximum allowed: {self.MAX_AGE}"
            )

        # ── Role Validation ──
        if not isinstance(role, UserRole):
            raise ValueError(
                f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
            )

        self.name = name
        self.email = email.lower()
        self.age = age
        self.role = role
        self.phone = phone
        self.address = address or {}
        self.is_active = True

    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
        self.touch()

    def update_address(self, address: Dict[str, str]):
        """Update user shipping address."""
        required = ["street", "city", "state", "zip_code"]
        missing = [f for f in required if f not in address]
        if missing:
            raise ValueError(f"Address missing required fields: {missing}")
        self.address = address
        self.touch()

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "name": self.name,
                "email": self.email,
                "age": self.age,
                "role": self.role.value,
                "phone": self.phone,
                "address": self.address,
                "is_active": self.is_active,
            }
        )
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            role=UserRole(data.get("role", "customer")),
            phone=data.get("phone"),
            address=data.get("address"),
            id=data.get("id"),
        )
