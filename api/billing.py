"""
Billing API — generates invoices from completed orders.

Builds itemized invoices with line-item breakdowns and regional
tax calculations. Designed to be called after order payment
is confirmed and the order record is fully populated.
"""

from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

from utils.database import get_user_by_id
from utils.logger import log_info, log_error
from utils.tax import calculate_tax, get_tax_breakdown


class BillingError(Exception):
    pass


class InvoiceGenerationError(BillingError):
    pass


async def generate_invoice(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an itemized invoice for a completed order.

    Builds line items from the order's product list, applies
    regional tax via utils/tax.py, and returns the full invoice.
    """
    invoice_id = f"INV-{uuid4().hex[:8].upper()}"

    try:
        user = await get_user_by_id(order_data["user_id"])
        user_name = user.get("name", "Unknown") if user else "Unknown"

        line_items = []
        subtotal = 0.0

        for product_entry in order_data["products"]:
            product_id = product_entry.get("product_id")
            quantity = product_entry.get("quantity", 1)
            unit_price = product_entry.get("unit_price", 0.0)
            line_total = round(quantity * unit_price, 2)
            subtotal += line_total

            line_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            })

        tax_amount = calculate_tax(subtotal, order_data["shipping_address"])
        tax_breakdown = get_tax_breakdown(subtotal, order_data["shipping_address"])
        total = round(subtotal + tax_amount, 2)

        invoice = {
            "invoice_id": invoice_id,
            "order_id": order_data.get("id", "N/A"),
            "user_id": order_data["user_id"],
            "user_name": user_name,
            "payment_status": order_data["payment_status"],
            "line_items": line_items,
            "subtotal": round(subtotal, 2),
            "tax": tax_amount,
            "tax_breakdown": tax_breakdown,
            "total": total,
            "created_at": datetime.utcnow().isoformat(),
        }

        log_info(
            message=f"Invoice {invoice_id} generated for ${total:.2f}",
            transaction_id=invoice_id,
            extra={"order_id": order_data.get("id"), "total": total},
        )

        return invoice

    except KeyError as e:
        log_error(
            error_message=f"Invoice generation failed — missing field {str(e)}",
            error_type="KeyError",
            transaction_id=invoice_id,
        )
        raise InvoiceGenerationError(f"Missing required order field: {str(e)}")


async def generate_bulk_invoices(
    orders: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate invoices for a list of orders.

    Processes each order independently. Failed invoices are
    recorded in the errors list; successful ones are returned.
    """
    batch_id = f"BULK-INV-{uuid4().hex[:8]}"
    results: Dict[str, Any] = {"invoices": [], "errors": []}

    for order in orders:
        try:
            invoice = await generate_invoice(order)
            results["invoices"].append(invoice)
        except BillingError as e:
            results["errors"].append({
                "order_id": order.get("id", "unknown"),
                "error": str(e),
            })

    log_info(
        message=(
            f"Bulk invoice complete: {len(results['invoices'])} generated, "
            f"{len(results['errors'])} failed"
        ),
        transaction_id=batch_id,
    )

    return results


async def get_invoice_summary(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a lightweight invoice summary without full line items.

    Used for quick display in order history and confirmation pages.
    """
    invoice_id = f"INV-SUM-{uuid4().hex[:8].upper()}"

    tax_amount = calculate_tax(
        order_data["total_amount"],
        order_data["shipping_address"],
    )

    return {
        "invoice_id": invoice_id,
        "order_id": order_data.get("id", "N/A"),
        "user_id": order_data["user_id"],
        "total_amount": order_data["total_amount"],
        "payment_status": order_data["payment_status"],
        "tax_amount": tax_amount,
        "payment_transaction_id": order_data["payment_transaction_id"],
        "created_at": datetime.utcnow().isoformat(),
    }
