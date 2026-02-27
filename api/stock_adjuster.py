"""
Stock Adjuster API — applies manual inventory corrections.

Used by warehouse staff to reconcile physical counts against
the system, write off damaged goods, and record supplier receipts.
All adjustments are logged for audit purposes.
"""

from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

from utils.database import update_inventory, get_product_by_id
from services.inventory_service import check_stock_availability
from config.settings import LOW_STOCK_THRESHOLD
from utils.logger import log_info, log_error, log_inventory_change


class StockAdjusterError(Exception):
    pass


async def apply_stock_adjustment(
    product_id: str,
    adjustment: int,
    reason: str,
) -> Dict[str, Any]:
    """
    Apply a signed stock adjustment to a product.

    Positive adjustment adds stock (e.g. supplier delivery).
    Negative adjustment removes stock (e.g. damaged goods write-off).
    """
    txn_id = f"ADJ-{uuid4().hex[:8]}"

    try:
        product_data = await get_product_by_id(product_id)
        if not product_data:
            raise StockAdjusterError(f"Product not found: {product_id}")

        current_qty = product_data.get("stock_quantity", 0)

        await update_inventory(product_id, adjustment)

        new_qty = current_qty + adjustment

        log_inventory_change(
            product_id=product_id,
            old_quantity=current_qty,
            new_quantity=new_qty,
            reason=reason,
        )

        log_info(
            message=f"Stock adjusted for {product_id}: {adjustment:+d} ({reason})",
            transaction_id=txn_id,
            extra={"product_id": product_id, "adjustment": adjustment},
        )

        return {
            "product_id": product_id,
            "adjustment": adjustment,
            "previous_quantity": current_qty,
            "updated_quantity": new_qty,
            "reason": reason,
            "adjusted_at": datetime.utcnow().isoformat(),
        }

    except StockAdjusterError:
        raise
    except ValueError as e:
        log_error(
            error_message=f"Stock adjustment failed for {product_id}: {str(e)}",
            error_type="ValueError",
            transaction_id=txn_id,
        )
        raise StockAdjusterError(str(e))


async def apply_batch_adjustments(
    adjustments: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Apply a list of stock adjustments in sequence.

    Processes each item independently. Failed items are
    recorded in the errors list; successful items proceed.
    """
    batch_id = f"BATCH-{uuid4().hex[:8]}"
    results: Dict[str, Any] = {"applied": [], "failed": [], "batch_id": batch_id}

    for adj in adjustments:
        product_id = adj.get("product_id", "")
        quantity = adj.get("quantity", 0)
        reason = adj.get("reason", "batch_adjustment")

        try:
            result = await apply_stock_adjustment(product_id, quantity, reason)
            results["applied"].append({
                "product_id": product_id,
                "adjustment": quantity,
                "updated_quantity": result["updated_quantity"],
            })
        except StockAdjusterError as e:
            results["failed"].append({"product_id": product_id, "error": str(e)})

    log_info(
        message=(
            f"Batch {batch_id}: {len(results['applied'])} applied, "
            f"{len(results['failed'])} failed"
        ),
        transaction_id=batch_id,
    )

    return results


async def reconcile_to_physical_count(
    product_id: str,
    actual_count: int,
) -> Dict[str, Any]:
    """
    Reconcile system inventory to match a physical warehouse count.

    Calculates the difference and applies an adjustment so the
    system quantity matches the count.
    """
    product_data = await get_product_by_id(product_id)
    if not product_data:
        raise StockAdjusterError(f"Product not found: {product_id}")

    system_qty = product_data.get("stock_quantity", 0)
    difference = actual_count - system_qty

    if difference == 0:
        return {
            "product_id": product_id,
            "adjustment": 0,
            "system_quantity": system_qty,
            "physical_count": actual_count,
            "message": "No adjustment required",
        }

    return await apply_stock_adjustment(
        product_id=product_id,
        adjustment=difference,
        reason=f"physical_count_reconciliation:system={system_qty},counted={actual_count}",
    )


async def get_low_stock_products(threshold: int = LOW_STOCK_THRESHOLD) -> List[str]:
    """Return product IDs where stock is at or below the given threshold."""
    # In production: query db.products where stock_quantity <= threshold
    return []
