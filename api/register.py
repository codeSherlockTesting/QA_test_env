"""
User Registration API endpoint.

Handles new user account creation and bulk registration.
Raises RegistrationError on validation or persistence failures.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

from models.user import User, UserRole
from utils.logger import log_info, log_error


class RegistrationError(Exception):
    pass


class DuplicateEmailError(RegistrationError):
    pass


def _prepare_registration_data(
    registration_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize raw registration input before constructing the user object.

    Strips whitespace, lowercases email, casts age to int,
    and applies a default role when not provided.
    """
    return {
        "name": str(registration_data["name"]).strip(),
        "email": str(registration_data["email"]).strip().lower(),
        "age": int(registration_data["age"]),
        "role": registration_data.get("role", "customer"),
        "phone": registration_data.get("phone"),
        "address": registration_data.get("address"),
    }


async def register_user(
    registration_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Register a new user account.

    Args:
        registration_data: Dict with name, email, age, role, phone, address

    Returns:
        Dict with user_id, status, email, and created_at

    Raises:
        RegistrationError: If registration fails
    """
    transaction_id = f"reg_{uuid4().hex[:10]}"

    try:
        log_info(
            message=f"Starting registration for {registration_data.get('email')}",
            transaction_id=transaction_id,
        )

        prepared = _prepare_registration_data(registration_data)

        user = User(
            name=prepared["name"],
            email=prepared["email"],
            age=prepared["age"],
            role=UserRole(prepared["role"]),
            phone=prepared["phone"],
            address=prepared["address"],
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
            error_message=f"Registration failed: {str(e)}",
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
