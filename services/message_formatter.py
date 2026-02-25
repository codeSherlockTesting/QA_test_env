"""
Message formatter for building notification content.

Formats email/notification content for various events.
Currently used by notification_service.
"""

from datetime import datetime
from typing import Dict, Any


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

    lines.extend(
        [
            "",
            f"Total: ${total:.2f}",
            "",
            "Thank you for your purchase!",
        ]
    )

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
