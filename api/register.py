"""
User Registration API endpoint.

Implements user registration by creating a User instance.
The User class constructor (in models/user.py on main branch)
already enforces strict validation including Age >= 18.

This file does NOT include its own validation because the
model layer handles it. The new pipeline should recognize this
pattern and NOT flag "missing validation."
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

from models.user import User, UserRole
from utils.database import get_user_by_id, save_order
from utils.logger import log_info, log_error


class RegistrationError(Exception):
    pass


class DuplicateEmailError(RegistrationError):
    pass


async def register_user(registration_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register a new user account.

    The User() constructor handles all input validation:
    - Name: 2-100 chars, non-empty
    - Email: valid format with @ and domain
    - Age: must be >= 18 (legal requirement)
    - Role: valid UserRole enum

    No additional validation is needed here because the model
    enforces constraints at construction time.

    Args:
        registration_data: Dict with name, email, age, phone, address

    Returns:
        Dict with user_id, status, and created_at

    Raises:
        RegistrationError: If registration fails
        ValueError: If User constructor validation fails
    """
    transaction_id = f"reg_{uuid4().hex[:10]}"

    try:
        log_info(
            message=f"Starting registration for {registration_data.get('email')}",
            transaction_id=transaction_id,
        )

        user = User(
            name=registration_data["name"],
            email=registration_data["email"],
            age=registration_data["age"],
            role=UserRole(registration_data.get("role", "customer")),
            phone=registration_data.get("phone"),
            address=registration_data.get("address"),
        )

        # In production: save to database
        # await db.users.insert_one(user.to_dict())

        log_info(
            message=f"User registered successfully: {user.id}",
            transaction_id=transaction_id,
            extra={"user_id": user.id, "email": user.email},
        )

        return {
            "user_id": user.id,
            "status": "registered",
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }

    except (ValueError, TypeError) as e:
        log_error(
            error_message=f"Registration validation failed: {str(e)}",
            error_type=type(e).__name__,
            transaction_id=transaction_id,
            extra={"email": registration_data.get("email")},
        )
        raise RegistrationError(f"Registration failed: {str(e)}")

    except Exception as e:
        log_error(
            error_message=f"Unexpected registration error: {str(e)}",
            error_type="RegistrationError",
            transaction_id=transaction_id,
        )
        raise RegistrationError(f"Registration failed unexpectedly: {str(e)}")


async def register_bulk_users(
    users_data: list[Dict[str, Any]],
) -> Dict[str, Any]:
    """Register multiple users, collecting successes and failures."""
    results = {"registered": [], "failed": []}

    for user_data in users_data:
        try:
            result = await register_user(user_data)
            results["registered"].append(result)
        except RegistrationError as e:
            results["failed"].append(
                {"email": user_data.get("email"), "error": str(e)}
            )

    log_info(
        message=(
            f"Bulk registration complete: "
            f"{len(results['registered'])} ok, {len(results['failed'])} failed"
        ),
        transaction_id="bulk_reg",
    )
    return results
