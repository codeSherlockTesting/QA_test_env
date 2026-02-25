"""
Message formatter for building notification content.

MODIFIED VERSION: This PR version adds a dependency back to
notification_service, creating a circular dependency:
  notification_service → message_formatter → notification_service

The pipeline should detect this circular reference, handle it
gracefully (no infinite loop), and complete analysis with
full context of both files.
"""

from datetime import datetime
from typing import Dict, Any, List

# CIRCULAR: This import creates a cycle with notification_service,
# which already imports from this module.
from services.notification_service import send_notification, NotificationError
from utils.logger import log_info, log_error


def format_order_confirmation(order_data: Dict[str, Any]) -> str:
    """Format an order confirmation message."""
    order_id = order_data.get("order_id", "N/A")
    total = order_data.get("total_amount", 0.0)
    items = order_data.get("products", [])

    lines = [
        f"Order Confirmation - {order_id}",
        f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Items:",
    ]

    for item in items:
        name = item.get("product_name", "Unknown")
        qty = item.get("quantity", 0)
        price = item.get("unit_price", 0.0)
        lines.append(f"  - {name} x{qty} @ ${price:.2f}")

    lines.extend(["", f"Total: ${total:.2f}", "", "Thank you for your purchase!"])
    return "\n".join(lines)


def format_shipping_update(shipping_data: Dict[str, Any]) -> str:
    """Format a shipping update message."""
    order_id = shipping_data.get("order_id", "N/A")
    tracking = shipping_data.get("tracking_number", "N/A")
    carrier = shipping_data.get("carrier", "Unknown")

    return (
        f"Shipping Update - Order {order_id}\n"
        f"Carrier: {carrier}\n"
        f"Tracking Number: {tracking}\n"
        f"Estimated Delivery: {shipping_data.get('estimated_delivery', 'TBD')}\n"
    )


def format_error_alert(error_data: Dict[str, Any]) -> str:
    """Format an error alert for internal monitoring."""
    return (
        f"[ALERT] Error in {error_data.get('service', 'unknown')}\n"
        f"Type: {error_data.get('error_type', 'unknown')}\n"
        f"Message: {error_data.get('message', 'No details')}\n"
        f"Time: {datetime.utcnow().isoformat()}\n"
    )


async def format_and_send_order_update(
    recipient_email: str,
    order_data: Dict[str, Any],
    update_type: str = "confirmation",
) -> bool:
    """
    NEW: Format a message and send it directly.

    This method creates the circular dependency by calling back
    into notification_service.send_notification().
    """
    try:
        if update_type == "confirmation":
            message = format_order_confirmation(order_data)
        elif update_type == "shipping":
            message = format_shipping_update(order_data)
        else:
            message = format_error_alert(order_data)

        log_info(
            message=f"Formatted {update_type} for {recipient_email}",
            transaction_id=order_data.get("order_id", "unknown"),
        )

        # This calls back into notification_service → circular
        return await send_notification(
            recipient_email=recipient_email,
            notification_type="order_confirmation",
            data=order_data,
        )

    except NotificationError as e:
        log_error(
            error_message=f"Failed to send formatted update: {str(e)}",
            error_type="NotificationError",
            transaction_id=order_data.get("order_id", "unknown"),
        )
        return False
