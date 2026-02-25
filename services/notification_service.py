"""
Notification service for sending customer communications.

Depends on message_formatter for building notification content.
"""

import asyncio
from typing import Dict, Any, List

from services.message_formatter import format_order_confirmation, format_shipping_update
from utils.logger import log_info, log_error


class NotificationError(Exception):
    pass


async def send_notification(
    recipient_email: str,
    notification_type: str,
    data: Dict[str, Any],
) -> bool:
    """
    Send a notification to a customer.

    Args:
        recipient_email: Customer email address
        notification_type: One of order_confirmation, shipping_update
        data: Notification payload data
    """
    try:
        if notification_type == "order_confirmation":
            message = format_order_confirmation(data)
        elif notification_type == "shipping_update":
            message = format_shipping_update(data)
        else:
            raise NotificationError(
                f"Unknown notification type: {notification_type}"
            )

        log_info(
            message=f"Sending {notification_type} to {recipient_email}",
            transaction_id=data.get("order_id", "unknown"),
        )

        # In production: await email_client.send(recipient_email, message)
        await asyncio.sleep(0.1)
        return True

    except Exception as e:
        log_error(
            error_message=f"Failed to send notification: {str(e)}",
            error_type="NotificationError",
            transaction_id=data.get("order_id", "unknown"),
        )
        raise NotificationError(str(e))


async def send_bulk_notifications(
    notifications: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Send multiple notifications, returns success/failure counts."""
    results = {"sent": 0, "failed": 0}
    for notif in notifications:
        try:
            await send_notification(
                notif["email"], notif["type"], notif["data"]
            )
            results["sent"] += 1
        except NotificationError:
            results["failed"] += 1
    return results
