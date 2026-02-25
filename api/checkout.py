"""
Checkout API with Step 1 input validation.

Step 1 validates and sanitizes all user input BEFORE passing
to the order creation pipeline. This file works in tandem with
models/order.py (Step 2) to provide multi-step validation.
"""

from typing import Dict, Any

from utils.validator import validate_email, validate_credit_card, validate_address
from utils.logger import log_info, log_error


class CheckoutValidationError(Exception):
    pass


async def validate_checkout_input(
    checkout_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Step 1: Input Validation and Sanitization.

    Validates:
    - Email format (RFC 5322)
    - Credit card number (Luhn algorithm)
    - Shipping address (required fields + ZIP code)
    - Items list (non-empty, valid quantities)
    - User ID (non-empty)

    This MUST run before creating an Order (Step 2 in models/order.py).
    """
    errors = []

    # ── Validate Email ──
    email = checkout_data.get("email", "")
    is_valid, error = validate_email(email)
    if not is_valid:
        errors.append(f"Email: {error}")

    # ── Validate Credit Card ──
    card_number = checkout_data.get("payment", {}).get("card_number", "")
    is_valid, error = validate_credit_card(card_number)
    if not is_valid:
        errors.append(f"Card: {error}")

    # ── Validate Shipping Address ──
    address = checkout_data.get("shipping_address", {})
    is_valid, error = validate_address(address)
    if not is_valid:
        errors.append(f"Address: {error}")

    # ── Validate Items ──
    items = checkout_data.get("items", [])
    if not items:
        errors.append("Items: Cart is empty")
    for i, item in enumerate(items):
        if "product_id" not in item:
            errors.append(f"Item {i}: missing product_id")
        if item.get("quantity", 0) <= 0:
            errors.append(f"Item {i}: quantity must be positive")

    # ── Validate User ID ──
    if not checkout_data.get("user_id"):
        errors.append("User ID is required")

    if errors:
        log_error(
            error_message=f"Checkout validation failed: {errors}",
            error_type="CheckoutValidationError",
            transaction_id=checkout_data.get("transaction_id", "unknown"),
            extra={"errors": errors},
        )
        raise CheckoutValidationError(
            f"Input validation failed with {len(errors)} error(s): "
            f"{'; '.join(errors)}"
        )

    log_info(
        message="Step 1 validation passed",
        transaction_id=checkout_data.get("transaction_id", "unknown"),
    )

    return {
        "user_id": checkout_data["user_id"],
        "email": email.strip().lower(),
        "items": items,
        "shipping_address": address,
        "payment": checkout_data["payment"],
    }
