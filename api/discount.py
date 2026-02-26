"""
Discount API — applies promotional discounts to orders and products.

Supports percentage discounts, flat-rate codes, and bulk
purchase pricing for high-quantity orders.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from models.order import Order, OrderItem, OrderStatus
from models.product import Product, ProductCategory
from config.settings import TAX_RATE, MIN_ORDER_AMOUNT, MAX_ORDER_AMOUNT
from utils.database import get_product_by_id, get_user_by_id, save_order
from utils.logger import log_info, log_error


class DiscountError(Exception):
    pass


DISCOUNT_CODES: Dict[str, Dict[str, Any]] = {
    "SAVE10": {"type": "percentage", "value": 10.0, "min_order": 50.0},
    "FLAT20": {"type": "flat", "value": 20.0, "min_order": 100.0},
    "BULK5": {"type": "percentage", "value": 5.0, "min_order": 200.0},
}


async def apply_discount_to_order(
    order: Order,
    discount_code: str,
) -> Dict[str, Any]:
    """
    Apply a discount code to an existing order.

    Validates the code, checks the order is in a modifiable state,
    and recalculates totals after discount.
    """
    txn_id = f"DISC-{uuid4().hex[:8]}"

    try:
        discount = DISCOUNT_CODES.get(discount_code.upper())
        if not discount:
            raise DiscountError(f"Invalid discount code: {discount_code}")

        if not order.can_cancel():
            raise DiscountError(
                f"Discount cannot be applied to orders in "
                f"'{order.status.value}' status"
            )

        if order.subtotal < discount["min_order"]:
            raise DiscountError(
                f"Order subtotal ${order.subtotal:.2f} is below minimum "
                f"${discount['min_order']:.2f} required for code '{discount_code}'"
            )

        if discount["type"] == "percentage":
            discount_amount = round(
                order.subtotal * (discount["value"] / 100), 2
            )
        else:
            discount_amount = min(discount["value"], order.subtotal)

        new_subtotal = round(order.subtotal - discount_amount, 2)
        new_tax = round(new_subtotal * TAX_RATE, 2)
        new_total = round(new_subtotal + new_tax, 2)

        if new_total < MIN_ORDER_AMOUNT:
            raise DiscountError(
                f"Discounted total ${new_total:.2f} falls below the "
                f"minimum order amount of ${MIN_ORDER_AMOUNT:.2f}"
            )

        log_info(
            message=(
                f"Discount '{discount_code}' applied to order "
                f"{order.order_id}: -{discount_amount:.2f}"
            ),
            transaction_id=txn_id,
            extra={
                "order_id": order.order_id,
                "original_total": order.total,
                "discount_amount": discount_amount,
                "new_total": new_total,
            },
        )

        return {
            "order_id": order.order_id,
            "discount_code": discount_code,
            "discount_type": discount["type"],
            "discount_amount": discount_amount,
            "original_total": order.total,
            "new_subtotal": new_subtotal,
            "new_tax": new_tax,
            "new_total": new_total,
        }

    except DiscountError:
        raise
    except Exception as e:
        log_error(
            error_message=f"Discount application failed: {str(e)}",
            error_type="DiscountError",
            transaction_id=txn_id,
        )
        raise DiscountError(str(e))


async def apply_bulk_discount(
    product_id: str,
    quantity: int,
    user_id: str,
) -> Dict[str, Any]:
    """
    Apply a bulk purchase discount for high-quantity orders.

    Determines discount tier based on quantity and adjusts
    unit price accordingly. Updates the product's stock count.
    """
    txn_id = f"BULK-{uuid4().hex[:8]}"

    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise DiscountError(f"User not found: {user_id}")

        product_data = await get_product_by_id(product_id)
        if not product_data:
            raise DiscountError(f"Product not found: {product_id}")

        product = Product(
            name=product_data["name"],
            price=product_data["price"],
            category=ProductCategory(product_data["category"]),
            stock_quantity=product_data.get("stock_quantity", 0),
        )

        if not product.is_in_stock():
            raise DiscountError(f"Product {product_id} is out of stock")

        product.update_stock(-quantity)

        base_price = product_data["price"]
        if quantity >= 50:
            discount_pct = 15.0
        elif quantity >= 20:
            discount_pct = 10.0
        elif quantity >= 10:
            discount_pct = 5.0
        else:
            discount_pct = 0.0

        unit_price = round(base_price * (1 - discount_pct / 100), 2)
        subtotal = round(unit_price * quantity, 2)
        tax = round(subtotal * TAX_RATE, 2)
        total = round(subtotal + tax, 2)

        log_info(
            message=f"Bulk discount {discount_pct}% applied for qty={quantity}",
            transaction_id=txn_id,
            extra={
                "product_id": product_id,
                "quantity": quantity,
                "discount_pct": discount_pct,
                "total": total,
            },
        )

        return {
            "product_id": product_id,
            "product_name": product_data["name"],
            "quantity": quantity,
            "base_price": base_price,
            "discount_percent": discount_pct,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
        }

    except DiscountError:
        raise
    except Exception as e:
        log_error(
            error_message=f"Bulk discount failed: {str(e)}",
            error_type="DiscountError",
            transaction_id=txn_id,
        )
        raise DiscountError(str(e))
