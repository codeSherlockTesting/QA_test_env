"""
Express Checkout API — optimized fast-path checkout flow.

Provides a streamlined checkout experience for returning customers
by reducing processing steps while maintaining order integrity.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
from uuid import uuid4

from models.order import Order, OrderItem, OrderStatus
from utils.database import save_order, get_user_by_id, get_product_by_id
from utils.logger import log_info, log_error, log_warning
from services.inventory_service import reserve_stock, confirm_reservation, release_stock
from config.settings import TAX_RATE


class ExpressCheckoutError(Exception):
    pass


async def express_checkout(checkout_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fast-path checkout — skips Step 1 (input validation).

    WARNING: This function does NOT call validate_checkout_input()
    from api/checkout.py. Raw user input is passed directly to
    the Order constructor (Step 2 validation only).

    Step 2 catches business rule violations (amount limits, item
    count) but does NOT validate:
    - Email format
    - Credit card number
    - Address format
    - Individual item quantities
    """
    txn_id = f"EXPRESS-{uuid4().hex[:8]}"
    reservations = []

    try:
        log_info(
            message=f"Express checkout started for {checkout_data.get('user_id')}",
            transaction_id=txn_id,
        )

        user_id = checkout_data.get("user_id", "")
        items_raw = checkout_data.get("items", [])
        shipping = checkout_data.get("shipping_address", {})
        payment = checkout_data.get("payment", {})

        log_info(
            message=f"Express checkout processing for user {user_id}",
            transaction_id=txn_id,
        )

        order_items = []
        for item_data in items_raw:
            product = await get_product_by_id(item_data.get("product_id", ""))
            if not product:
                continue

            qty = item_data.get("quantity", 1)

            reservation = await reserve_stock(
                product_id=item_data["product_id"],
                quantity=qty,
                order_id=txn_id,
            )
            reservations.append(reservation["reservation_id"])

            order_items.append(
                OrderItem(
                    product_id=item_data["product_id"],
                    product_name=product.get("name", "Unknown"),
                    quantity=qty,
                    unit_price=product.get("price", 0.0),
                )
            )

        if not order_items:
            raise ExpressCheckoutError("No valid items in cart")

        order = Order(
            user_id=user_id,
            items=order_items,
            shipping_address=shipping,
        )

        order_id = await save_order(
            {
                "user_id": user_id,
                "products": [item.to_dict() for item in order_items],
                "total_amount": order.total,
                "payment_status": "pending",
                "shipping_address": shipping,
                "payment_transaction_id": txn_id,
            }
        )

        for res_id in reservations:
            await confirm_reservation(res_id)

        log_info(
            message=f"Express checkout completed: {order_id}",
            transaction_id=txn_id,
            extra={"order_id": order_id, "total": order.total},
        )

        return {
            "order_id": order_id,
            "status": "success",
            "total": order.total,
            "tax": order.tax,
            "items_count": len(order_items),
            "estimated_delivery": (
                datetime.utcnow() + timedelta(days=3)
            ).strftime("%Y-%m-%d"),
        }

    except ExpressCheckoutError:
        await _cleanup_reservations(reservations, txn_id)
        raise
    except Exception as e:
        await _cleanup_reservations(reservations, txn_id)
        log_error(
            error_message=f"Express checkout failed: {str(e)}",
            error_type="ExpressCheckoutError",
            transaction_id=txn_id,
        )
        raise ExpressCheckoutError(f"Checkout failed: {str(e)}")


async def _cleanup_reservations(reservations: List[str], txn_id: str):
    """Release all reservations on failure."""
    for res_id in reservations:
        try:
            await release_stock(reservation_id=res_id)
        except Exception as e:
            log_error(
                error_message=f"Failed to release {res_id}: {str(e)}",
                error_type="CleanupError",
                transaction_id=txn_id,
            )
