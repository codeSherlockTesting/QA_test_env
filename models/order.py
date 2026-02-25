"""
Order model with multi-step validation.

Step 2 Validation: Validates order business rules including
amount limits, item count, and data integrity. This validation
is called AFTER Step 1 (input sanitization in api/checkout.py).
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, List
from uuid import uuid4

from config.settings import TAX_RATE, MAX_ORDER_AMOUNT, MIN_ORDER_AMOUNT


class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class OrderItem:
    """Individual item within an order."""

    def __init__(
        self, product_id: str, product_name: str, quantity: int, unit_price: float
    ):
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if unit_price < 0:
            raise ValueError(f"Unit price cannot be negative, got {unit_price}")

        self.item_id = uuid4().hex[:8]
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = round(unit_price, 2)
        self.total_price = round(quantity * unit_price, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
        }


class Order:
    """
    Order model with Step 2 validation.

    Step 2 validates business rules:
    - Total amount within allowed range
    - At least one item present
    - All items have valid quantities
    - Tax calculation correctness
    - Shipping address completeness
    """

    def __init__(
        self, user_id: str, items: List[OrderItem], shipping_address: Dict[str, str]
    ):
        self.order_id = f"ORD-{uuid4().hex[:10].upper()}"
        self.user_id = user_id
        self.items = items
        self.shipping_address = shipping_address
        self.status = OrderStatus.PENDING
        self.created_at = datetime.utcnow()
        self.payment_id = None

        self.subtotal = sum(item.total_price for item in items)
        self.tax = round(self.subtotal * TAX_RATE, 2)
        self.total = round(self.subtotal + self.tax, 2)

        # ── STEP 2 VALIDATION ──
        self._validate_order()

    def _validate_order(self):
        """
        Step 2: Business rule validation.

        Runs AFTER Step 1 (input sanitization in api/checkout.py).
        Validates financial and business constraints.
        """
        if not self.items:
            raise ValueError("Order must contain at least one item")

        if len(self.items) > 100:
            raise ValueError(
                f"Order cannot exceed 100 items, got {len(self.items)}"
            )

        if self.total < MIN_ORDER_AMOUNT:
            raise ValueError(
                f"Order total ${self.total:.2f} is below "
                f"minimum ${MIN_ORDER_AMOUNT:.2f}"
            )

        if self.total > MAX_ORDER_AMOUNT:
            raise ValueError(
                f"Order total ${self.total:.2f} exceeds "
                f"maximum ${MAX_ORDER_AMOUNT:.2f}"
            )

        for item in self.items:
            if item.quantity > 999:
                raise ValueError(
                    f"Item '{item.product_name}' quantity "
                    f"{item.quantity} exceeds limit of 999"
                )

        required_addr = ["street", "city", "state", "zip_code"]
        missing = [f for f in required_addr if f not in self.shipping_address]
        if missing:
            raise ValueError(f"Shipping address missing: {missing}")

    def update_status(self, new_status: OrderStatus):
        allowed = {
            OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.PAID, OrderStatus.CANCELLED],
            OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.REFUNDED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        }
        if new_status not in allowed.get(self.status, []):
            raise ValueError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status

    def can_cancel(self) -> bool:
        return self.status in (OrderStatus.PENDING, OrderStatus.PROCESSING)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "status": self.status.value,
            "shipping_address": self.shipping_address,
            "payment_id": self.payment_id,
            "created_at": self.created_at.isoformat(),
        }
