"""
Inventory management service with concurrency-safe stock reservation.

Uses asyncio locks to prevent race conditions during concurrent
stock operations. All stock modifications MUST go through this
service to maintain data integrity.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from uuid import uuid4

from config.settings import RESERVATION_TIMEOUT_MINUTES
from utils.logger import log_info, log_inventory_change


# ── Critical: Reservation lock for concurrency safety ──
# All stock modifications MUST acquire this lock to prevent
# double-selling and race conditions.
_reservation_lock = asyncio.Lock()

_reservations: Dict[str, Dict[str, Any]] = {}
_stock: Dict[str, int] = {}


async def reserve_stock(
    product_id: str, quantity: int, order_id: str
) -> Dict[str, Any]:
    """
    Reserve stock for an order.
    Acquires _reservation_lock to prevent concurrent modifications.
    """
    async with _reservation_lock:
        current_stock = _stock.get(product_id, 0)
        if current_stock < quantity:
            raise InsufficientStockError(
                f"Cannot reserve {quantity} units of {product_id}. "
                f"Available: {current_stock}"
            )

        reservation_id = f"RSV-{uuid4().hex[:8]}"
        _stock[product_id] = current_stock - quantity
        _reservations[reservation_id] = {
            "reservation_id": reservation_id,
            "product_id": product_id,
            "quantity": quantity,
            "order_id": order_id,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow()
            + timedelta(minutes=RESERVATION_TIMEOUT_MINUTES),
            "confirmed": False,
        }

        log_inventory_change(
            product_id=product_id,
            old_quantity=current_stock,
            new_quantity=_stock[product_id],
            reason=f"Reserved for order {order_id}",
            transaction_id=order_id,
        )

        return _reservations[reservation_id]


async def confirm_reservation(reservation_id: str) -> bool:
    """Confirm a stock reservation after successful payment."""
    async with _reservation_lock:
        reservation = _reservations.get(reservation_id)
        if not reservation:
            raise ValueError(f"Reservation not found: {reservation_id}")
        if reservation["confirmed"]:
            raise ValueError(f"Reservation already confirmed: {reservation_id}")
        reservation["confirmed"] = True
        return True


async def release_stock(reservation_id: str) -> bool:
    """Release a stock reservation (e.g., on payment failure)."""
    async with _reservation_lock:
        reservation = _reservations.pop(reservation_id, None)
        if not reservation:
            return False
        product_id = reservation["product_id"]
        _stock[product_id] = _stock.get(product_id, 0) + reservation["quantity"]

        log_inventory_change(
            product_id=product_id,
            old_quantity=_stock[product_id] - reservation["quantity"],
            new_quantity=_stock[product_id],
            reason=f"Released reservation {reservation_id}",
        )
        return True


async def check_stock_availability(
    product_id: str, quantity: int
) -> Tuple[bool, int]:
    """Check if enough stock is available."""
    current = _stock.get(product_id, 0)
    return current >= quantity, current


async def update_stock_direct(product_id: str, quantity_change: int) -> int:
    """
    Directly update stock — MUST use _reservation_lock.

    WARNING: External callers should use reserve_stock() instead.
    This method is for internal inventory adjustments only.
    """
    async with _reservation_lock:
        current = _stock.get(product_id, 0)
        new_qty = current + quantity_change
        if new_qty < 0:
            raise ValueError(f"Stock cannot go negative for {product_id}")
        _stock[product_id] = new_qty
        return new_qty


class InsufficientStockError(Exception):
    """Raised when there is not enough stock for an operation."""

    pass
