"""
Status Notifier — sends customer-facing order status notifications.

Wraps the platform notification service with order-specific
message payloads for each fulfillment event type.
"""

from typing import Dict, Any
from models.order import Order, OrderStatus
from services.notification_service import send_notification, NotificationError
from utils.logger import log_info, log_error


class StatusNotifierError(Exception):
    pass


class StatusNotifier:
    """Dispatches order lifecycle notifications to customers."""

    async def send_shipping_confirmation(
        self,
        order: Order,
        tracking_number: str,
        carrier: str,
    ) -> bool:
        """Notify customer that their order has shipped."""
        try:
            await send_notification(
                recipient_email=f"customer-{order.user_id}@example.com",
                notification_type="shipping_update",
                data={
                    "order_id": order.order_id,
                    "tracking_number": tracking_number,
                    "carrier": carrier,
                    "total": order.total,
                },
            )

            log_info(
                message=f"Shipping notification sent for order {order.order_id}",
                transaction_id=order.order_id,
            )
            return True

        except Exception as e:
            log_error(
                error_message=f"Shipping notification failed: {str(e)}",
                error_type="NotificationError",
                transaction_id=order.order_id,
            )
            return False

    async def send_delivery_confirmation(self, order: Order) -> bool:
        """Notify customer that their order has been delivered."""
        try:
            await send_notification(
                recipient_email=f"customer-{order.user_id}@example.com",
                notification_type="order_confirmation",
                data={
                    "order_id": order.order_id,
                    "status": OrderStatus.DELIVERED.value,
                },
            )

            log_info(
                message=f"Delivery notification sent for order {order.order_id}",
                transaction_id=order.order_id,
            )
            return True

        except Exception as e:
            log_error(
                error_message=f"Delivery notification failed: {str(e)}",
                error_type="NotificationError",
                transaction_id=order.order_id,
            )
            return False

    async def send_cancellation_notice(
        self,
        order: Order,
        reason: str,
    ) -> bool:
        """Notify customer that their order has been cancelled."""
        try:
            await send_notification(
                recipient_email=f"customer-{order.user_id}@example.com",
                notification_type="order_confirmation",
                data={
                    "order_id": order.order_id,
                    "status": OrderStatus.CANCELLED.value,
                    "reason": reason,
                },
            )

            log_info(
                message=f"Cancellation notice sent for order {order.order_id}",
                transaction_id=order.order_id,
            )
            return True

        except Exception as e:
            log_error(
                error_message=f"Cancellation notification failed: {str(e)}",
                error_type="NotificationError",
                transaction_id=order.order_id,
            )
            return False
