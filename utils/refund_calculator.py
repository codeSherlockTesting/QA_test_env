"""
Refund calculation utilities.

Computes refund amounts based on item prices, quantities,
return eligibility windows, and tax reversal using the
centralized tax configuration.
"""

from typing import Dict, Any, List, Tuple

from config.settings import TAX_RATE
from models.order import OrderStatus


RETURN_WINDOW_DAYS = 30
NON_RETURNABLE_CATEGORIES = ["electronics", "books"]


class RefundError(Exception):
    pass


class RefundCalculator:
    """Calculates refund amounts and checks return eligibility."""

    def calculate_refund(self, items: List[Dict[str, Any]]) -> float:
        """
        Calculate total refund including tax reversal.

        Sums item line totals and adds back the tax that was
        originally charged, using TAX_RATE from config.
        """
        if not items:
            return 0.0

        subtotal = sum(
            item.get("unit_price", 0.0) * item.get("quantity", 1)
            for item in items
        )
        tax_credit = round(subtotal * TAX_RATE, 2)
        return round(subtotal + tax_credit, 2)

    def check_eligibility(self, item: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check if an item qualifies for return.

        Validates category eligibility and return window.
        """
        category = item.get("category", "").lower()
        if category in NON_RETURNABLE_CATEGORIES:
            return False, f"Category '{category}' is non-returnable"

        days_since_purchase = item.get("days_since_purchase", 0)
        if days_since_purchase > RETURN_WINDOW_DAYS:
            return (
                False,
                f"Return window of {RETURN_WINDOW_DAYS} days has expired",
            )

        if item.get("quantity", 1) <= 0:
            return False, "Quantity must be at least 1"

        return True, ""

    def calculate_partial_refund(
        self, item: Dict[str, Any], return_quantity: int
    ) -> float:
        """Calculate refund for a partial return of one item."""
        unit_price = item.get("unit_price", 0.0)
        subtotal = round(unit_price * return_quantity, 2)
        tax_credit = round(subtotal * TAX_RATE, 2)
        return round(subtotal + tax_credit, 2)
