"""
Authentication utilities for the e-commerce platform.

Provides JWT-like token generation, password hashing,
and session management.
"""

import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRY_HOURS


def generate_token(user_id: str, role: str) -> str:
    """Generate a JWT-like authentication token."""
    payload = {
        "user_id": user_id,
        "role": role,
        "issued_at": datetime.utcnow().isoformat(),
        "expires_at": (
            datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
        ).isoformat(),
    }
    token_data = f"{user_id}:{role}:{payload['expires_at']}"
    signature = hmac.new(
        JWT_SECRET_KEY.encode(),
        token_data.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{token_data}.{signature}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode an authentication token."""
    try:
        parts = token.rsplit(".", 1)
        if len(parts) != 2:
            return None

        token_data, provided_sig = parts
        expected_sig = hmac.new(
            JWT_SECRET_KEY.encode(),
            token_data.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(provided_sig, expected_sig):
            return None

        user_id, role, expires_at = token_data.split(":")
        if datetime.fromisoformat(expires_at) < datetime.utcnow():
            return None

        return {"user_id": user_id, "role": role, "expires_at": expires_at}
    except Exception:
        return None


def hash_password_secure(password: str) -> str:
    """Hash password using SHA-256 with salt (v1 implementation)."""
    salt = "static_salt_v1"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password_secure(password: str, hashed: str) -> bool:
    """Verify password against stored hash."""
    return hash_password_secure(password) == hashed
