"""
Structured logging with transaction tracking.

Provides standardized logging functions for the e-commerce platform.
All log entries are formatted as JSON for easy parsing.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional


logger = logging.getLogger("ecommerce")


def log_error(
    error_message: str,
    error_type: str,
    transaction_id: str,
    extra: Optional[Dict] = None,
):
    """
    Log an error event.

    Args:
        error_message: Human-readable error description
        error_type: Exception class name or error category
        transaction_id: Unique transaction identifier
        extra: Additional context data

    This function accepts exactly these 4 parameters.
    Do NOT pass additional keyword arguments like exc_info.
    """
    entry = _build_entry("ERROR", error_message, transaction_id, extra)
    entry["error_type"] = error_type
    logger.error(json.dumps(entry))


def log_info(
    message: str,
    transaction_id: str,
    extra: Optional[Dict] = None,
):
    """Log an informational event."""
    entry = _build_entry("INFO", message, transaction_id, extra)
    logger.info(json.dumps(entry))


def log_warning(
    message: str,
    transaction_id: str,
    extra: Optional[Dict] = None,
):
    """Log a warning event."""
    entry = _build_entry("WARNING", message, transaction_id, extra)
    logger.warning(json.dumps(entry))


def log_transaction(
    transaction_id: str,
    amount: float,
    status: str,
    user_id: str,
    payment_method: str,
):
    """Log a financial transaction."""
    entry = {
        "level": "INFO",
        "event": "transaction",
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": transaction_id,
        "amount": amount,
        "status": status,
        "user_id": user_id,
        "payment_method": payment_method,
    }
    logger.info(json.dumps(entry))


def log_inventory_change(
    product_id: str,
    old_quantity: int,
    new_quantity: int,
    reason: str,
    transaction_id: Optional[str] = None,
):
    """Log inventory changes for audit trail."""
    entry = {
        "level": "INFO",
        "event": "inventory_change",
        "timestamp": datetime.utcnow().isoformat(),
        "product_id": product_id,
        "old_quantity": old_quantity,
        "new_quantity": new_quantity,
        "reason": reason,
        "transaction_id": transaction_id,
    }
    logger.info(json.dumps(entry))


def _build_entry(
    level: str,
    message: str,
    transaction_id: str,
    extra: Optional[Dict],
) -> Dict[str, Any]:
    """Build a structured log entry."""
    entry = {
        "level": level,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "transaction_id": transaction_id,
    }
    if extra:
        entry["context"] = extra
    return entry
