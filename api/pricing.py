"""
Pricing API — calculates product prices with tax.

BUG: This module hardcodes TAX_RATE = 0.10 instead of importing
the centralized TAX_RATE (0.08) from config/settings.py.

The new pipeline should:
1. Fetch config/settings.py from main
2. Detect that TAX_RATE is defined there as 0.08
3. Flag the hardcoded 0.10 as "Constant Mismatch" or
   "Hardcoded Configuration"

The old pipeline (without fetching main) will see 0.10 as just
a local number and will not flag anything.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.database import get_product_by_id
from utils.logger import log_info, log_error


class PricingError(Exception):
    pass


# BUG: Hardcoded tax rate instead of using config.settings.TAX_RATE
# The centralized config defines TAX_RATE = 0.08, but this uses 0.10
TAX_RATE = 0.10


async def calculate_product_price(
    product_id: str,
    quantity: int = 1,
    discount_percent: float = 0.0,
    include_tax: bool = True,
) -> Dict[str, Any]:
    """
    Calculate the final price for a product.

    Uses a HARDCODED TAX_RATE instead of the centralized config.
    This creates an inconsistency where this endpoint charges
    10% tax while the rest of the system charges 8%.

    Args:
        product_id: Product to price
        quantity: Number of units
        discount_percent: Discount to apply (0-100)
        include_tax: Whether to include tax

    Returns:
        Price breakdown dict
    """
    calc_id = f"PRICE-{uuid4().hex[:8]}"

    try:
        product = await get_product_by_id(product_id)
        if not product:
            raise PricingError(f"Product not found: {product_id}")

        unit_price = product.get("price", 0.0)
        subtotal = round(unit_price * quantity, 2)

        discount_amount = 0.0
        if 0 < discount_percent <= 100:
            discount_amount = round(subtotal * (discount_percent / 100), 2)

        after_discount = round(subtotal - discount_amount, 2)

        # BUG: Using local TAX_RATE (0.10) instead of config TAX_RATE (0.08)
        tax_amount = round(after_discount * TAX_RATE, 2) if include_tax else 0.0
        total = round(after_discount + tax_amount, 2)

        log_info(
            message=f"Price calculated for {product_id}: ${total:.2f}",
            transaction_id=calc_id,
            extra={
                "product_id": product_id,
                "quantity": quantity,
                "tax_rate_used": TAX_RATE,
            },
        )

        return {
            "product_id": product_id,
            "product_name": product.get("name", "Unknown"),
            "unit_price": unit_price,
            "quantity": quantity,
            "subtotal": subtotal,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "after_discount": after_discount,
            "tax_rate": TAX_RATE,
            "tax_amount": tax_amount,
            "total": total,
        }

    except PricingError:
        raise
    except Exception as e:
        log_error(
            error_message=f"Pricing calculation failed: {str(e)}",
            error_type="PricingError",
            transaction_id=calc_id,
        )
        raise PricingError(f"Failed to calculate price: {str(e)}")


async def calculate_cart_total(
    items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Calculate total for multiple items using hardcoded TAX_RATE."""
    cart_subtotal = 0.0
    line_items = []

    for item in items:
        result = await calculate_product_price(
            product_id=item["product_id"],
            quantity=item.get("quantity", 1),
            discount_percent=item.get("discount", 0.0),
            include_tax=False,
        )
        cart_subtotal += result["after_discount"]
        line_items.append(result)

    # Same bug: using local TAX_RATE
    cart_tax = round(cart_subtotal * TAX_RATE, 2)
    cart_total = round(cart_subtotal + cart_tax, 2)

    return {
        "items": line_items,
        "subtotal": cart_subtotal,
        "tax_rate": TAX_RATE,
        "tax": cart_tax,
        "total": cart_total,
    }
