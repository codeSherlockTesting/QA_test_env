"""
Order Status API — manages order fulfillment lifecycle.

Handles shipping dispatch, delivery confirmation, and cancellation.
Notifies customers at each status transition via StatusNotifier.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

from services.status_notifier import StatusNotifier, StatusNotifierError
from models.order import Order, OrderStatus
from utils.database import update_order_status
from utils.logger import log_info, log_error, log_transaction


class OrderStatusError(Exception):
    pass


async def mark_as_shipped(
    order: Order,
    tracking_number: str,
    carrier: str = "standard",
) -> Dict[str, Any]:
    """
    Advance an order to SHIPPED and notify the customer.

    Persists the new status, attaches tracking details,
    and dispatches a shipping confirmation via StatusNotifier.
    """
    txn_id = f"SHIP-{uuid4().hex[:8]}"

    try:
        order.update_status(OrderStatus.SHIPPED)

        await update_order_status(order.order_id, OrderStatus.SHIPPED.value)

        notifier = StatusNotifier()
        await notifier.send_shipping_confirmation(
            order=order,
            tracking_number=tracking_number,
            carrier=carrier,
        )

        log_info(
            message=f"Order {order.order_id} marked as shipped",
            transaction_id=txn_id,
            extra={
                "order_id": order.order_id,
                "tracking_number": tracking_number,
                "carrier": carrier,
            },
        )

        return {
            "order_id": order.order_id,
            "status": OrderStatus.SHIPPED.value,
            "tracking_number": tracking_number,
            "carrier": carrier,
            "shipped_at": datetime.utcnow().isoformat(),
        }

    except ValueError as e:
        log_error(
            error_message=f"Ship order failed: {str(e)}",
            error_type="OrderTransitionError",
            transaction_id=txn_id,
            extra={"order_id": order.order_id},
        )
        raise OrderStatusError(str(e))


async def mark_as_delivered(order: Order) -> Dict[str, Any]:
    """Record that a shipped order has been delivered."""
    txn_id = f"DELIV-{uuid4().hex[:8]}"

    try:
        order.update_status(OrderStatus.DELIVERED)

        await update_order_status(order.order_id, OrderStatus.DELIVERED.value)

        notifier = StatusNotifier()
        await notifier.send_delivery_confirmation(order=order)

        log_info(
            message=f"Order {order.order_id} marked as delivered",
            transaction_id=txn_id,
            extra={"order_id": order.order_id},
        )

        return {
            "order_id": order.order_id,
            "status": OrderStatus.DELIVERED.value,
            "delivered_at": datetime.utcnow().isoformat(),
        }

    except ValueError as e:
        log_error(
            error_message=f"Delivery confirmation failed: {str(e)}",
            error_type="OrderTransitionError",
            transaction_id=txn_id,
        )
        raise OrderStatusError(str(e))


async def cancel_order(
    order: Order,
    user_id: str,
    reason: str,
) -> Dict[str, Any]:
    """
    Cancel an order and notify the customer.

    Applies cancellation, persists the status, and sends
    a cancellation notice via StatusNotifier.
    """
    txn_id = f"CANCEL-{uuid4().hex[:8]}"

    try:
        order.update_status(OrderStatus.CANCELLED)

        await update_order_status(order.order_id, OrderStatus.CANCELLED.value)

        notifier = StatusNotifier()
        await notifier.send_cancellation_notice(order=order, reason=reason)

        log_info(
            message=f"Order {order.order_id} cancelled by user {user_id}",
            transaction_id=txn_id,
            extra={"reason": reason, "user_id": user_id},
        )

        return {
            "order_id": order.order_id,
            "status": OrderStatus.CANCELLED.value,
            "reason": reason,
            "cancelled_at": datetime.utcnow().isoformat(),
        }

    except ValueError as e:
        log_error(
            error_message=f"Order cancellation failed: {str(e)}",
            error_type="OrderTransitionError",
            transaction_id=txn_id,
        )
        raise OrderStatusError(str(e))
