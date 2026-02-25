"""
Billing API — generates invoices from order data.

This file depends on:
- utils/database.py (main branch) for ORDER_SCHEMA and data retrieval
- utils/tax.py (included in THIS PR) for tax calculations

The pipeline should combine PR-context (billing.py + tax.py) with
main-context (database.py) to validate the full data flow chain
with zero false positives about "unknown data shape."
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.database import (
    ORDER_SCHEMA,
    validate_against_schema,
    get_user_by_id,
    get_product_by_id,
)
from utils.logger import log_info, log_error
from utils.tax import calculate_tax, get_tax_breakdown


class BillingError(Exception):
    pass


class InvoiceGenerationError(BillingError):
    pass


async def generate_invoice(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an invoice from order data.

    Uses ORDER_SCHEMA from database.py to validate the input shape,
    then applies tax calculations from utils/tax.py (in this PR).

    Args:
        order_data: Order data matching ORDER_SCHEMA from database.py

    Returns:
        Invoice dict with line items, taxes, and totals
    """
    invoice_id = f"INV-{uuid4().hex[:8].upper()}"

    schema_errors = validate_against_schema(order_data, ORDER_SCHEMA)
    if schema_errors:
        log_error(
            error_message=f"Invoice data validation failed: {schema_errors}",
            error_type="SchemaValidationError",
            transaction_id=invoice_id,
            extra={"errors": schema_errors},
        )
        raise InvoiceGenerationError(
            f"Invalid order data: {'; '.join(schema_errors)}"
        )

    user = await get_user_by_id(order_data["user_id"])
    user_name = user.get("name", "Unknown") if user else "Unknown"

    line_items = []
    subtotal = 0.0

    for product_entry in order_data.get("products", []):
        product_id = product_entry.get("product_id")
        quantity = product_entry.get("quantity", 1)
        unit_price = product_entry.get("unit_price", 0.0)
        line_total = round(quantity * unit_price, 2)
        subtotal += line_total

        line_items.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    tax_result = calculate_tax(subtotal, order_data.get("shipping_address", {}))
    tax_breakdown = get_tax_breakdown(
        subtotal, order_data.get("shipping_address", {})
    )

    total = round(subtotal + tax_result, 2)

    invoice = {
        "invoice_id": invoice_id,
        "order_id": order_data.get("id", "N/A"),
        "user_id": order_data["user_id"],
        "user_name": user_name,
        "line_items": line_items,
        "subtotal": subtotal,
        "tax": tax_result,
        "tax_breakdown": tax_breakdown,
        "total": total,
        "payment_status": order_data.get("payment_status", "pending"),
        "created_at": datetime.utcnow().isoformat(),
    }

    log_info(
        message=f"Invoice generated: {invoice_id} for ${total:.2f}",
        transaction_id=invoice_id,
        extra={"order_id": order_data.get("id"), "total": total},
    )

    return invoice


async def generate_bulk_invoices(
    orders: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Generate invoices for multiple orders."""
    results = {"invoices": [], "errors": []}

    for order in orders:
        try:
            invoice = await generate_invoice(order)
            results["invoices"].append(invoice)
        except BillingError as e:
            results["errors"].append(
                {"order_id": order.get("id", "unknown"), "error": str(e)}
            )

    return results
