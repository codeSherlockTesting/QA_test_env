"""
Input validation utilities.

Provides validation functions for email, credit card,
address, and phone number inputs.
"""

import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format (RFC 5322 simplified)."""
    if not email or not isinstance(email, str):
        return False, "Email is required"

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, f"Invalid email format: {email}"

    return True, ""


def validate_credit_card(card_number: str) -> Tuple[bool, str]:
    """Validate credit card number using Luhn algorithm."""
    if not card_number or not isinstance(card_number, str):
        return False, "Card number is required"

    cleaned = card_number.replace(" ", "").replace("-", "")
    if not cleaned.isdigit():
        return False, "Card number must contain only digits"
    if len(cleaned) < 13 or len(cleaned) > 19:
        return False, "Card number must be 13-19 digits"

    total = 0
    reverse = cleaned[::-1]
    for i, digit in enumerate(reverse):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    if total % 10 != 0:
        return False, "Invalid card number (failed checksum)"

    return True, ""


def validate_address(address: dict) -> Tuple[bool, str]:
    """Validate a physical address."""
    if not address or not isinstance(address, dict):
        return False, "Address is required"

    required_fields = ["street", "city", "state", "zip_code"]
    for field in required_fields:
        if field not in address or not address[field]:
            return False, f"Missing required field: {field}"

    zip_code = str(address["zip_code"])
    if not re.match(r"^\d{5}(-\d{4})?$", zip_code):
        return False, f"Invalid ZIP code: {zip_code}"

    return True, ""


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """Validate phone number format."""
    if not phone:
        return False, "Phone number is required"

    cleaned = re.sub(r"[\s\-\(\)\+]", "", phone)
    if not cleaned.isdigit():
        return False, "Phone number must contain only digits"
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number must be 10-15 digits"

    return True, ""
