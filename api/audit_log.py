"""
Audit Log API — records significant business events for compliance.

Tracks order lifecycle events, inventory adjustments, and
payment activity for regulatory and operational audit trails.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.logger import log_info, log_error, log_inventory_change, log_transaction
from utils.database import get_user_by_id, get_product_by_id, update_order_status
from services.inventory_service import check_stock_availability


class AuditError(Exception):
    pass


_audit_records: List[Dict[str, Any]] = []


async def record_order_event(
    order_id: str,
    user_id: str,
    event_type: str,
    details: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Record an order lifecycle event in the audit log.

    Captures user info alongside the event for a complete trace.
    """
    audit_id = f"AUDIT-{uuid4().hex[:8]}"

    user = await get_user_by_id(user_id)
    user_email = user.get("email", "unknown") if user else "unknown"

    record = {
        "audit_id": audit_id,
        "event_type": event_type,
        "order_id": order_id,
        "user_id": user_id,
        "user_email": user_email,
        "details": details,
        "recorded_at": datetime.utcnow().isoformat(),
    }

    _audit_records.append(record)

    log_info(
        message=f"Audit event '{event_type}' recorded for order {order_id}",
        transaction_id=audit_id,
    )

    return record


async def record_inventory_adjustment(
    product_id: str,
    old_quantity: int,
    new_quantity: int,
    reason: str,
) -> Dict[str, Any]:
    """
    Record an inventory change for the audit trail.

    Calls log_inventory_change to persist the change to the
    structured log store alongside the local audit record.
    """
    audit_id = f"INV-AUDIT-{uuid4().hex[:8]}"

    product_data = await get_product_by_id(product_id)
    product_name = (
        product_data.get("name", "Unknown") if product_data else "Unknown"
    )

    log_inventory_change(
        product_id=product_id,
        old_quantity=old_quantity,
        new_quantity=new_quantity,
        reason=reason,
    )

    record = {
        "audit_id": audit_id,
        "event_type": "inventory_adjustment",
        "product_id": product_id,
        "product_name": product_name,
        "old_quantity": old_quantity,
        "new_quantity": new_quantity,
        "change": new_quantity - old_quantity,
        "reason": reason,
        "recorded_at": datetime.utcnow().isoformat(),
    }

    _audit_records.append(record)
    return record


async def record_payment_event(
    transaction_id: str,
    amount: float,
    status: str,
    user_id: str,
) -> Dict[str, Any]:
    """Record a payment event in the audit trail."""
    audit_id = f"PAY-AUDIT-{uuid4().hex[:8]}"

    log_transaction(
        transaction_id=transaction_id,
        amount=amount,
        status=status,
        user_id=user_id,
        payment_method="credit_card",
    )

    log_info(
        message=f"Payment event recorded: {transaction_id}",
        transaction_id=audit_id,
    )

    record = {
        "audit_id": audit_id,
        "event_type": "payment",
        "transaction_id": transaction_id,
        "amount": amount,
        "status": status,
        "user_id": user_id,
        "recorded_at": datetime.utcnow().isoformat(),
    }

    _audit_records.append(record)
    return record


async def get_audit_trail(
    order_id: Optional[str] = None,
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieve audit records matching the given filters."""
    results = list(_audit_records)

    if order_id:
        results = [r for r in results if r.get("order_id") == order_id]
    if user_id:
        results = [r for r in results if r.get("user_id") == user_id]
    if event_type:
        results = [r for r in results if r.get("event_type") == event_type]

    return sorted(results, key=lambda r: r["recorded_at"], reverse=True)


async def check_stock_audit(product_ids: List[str]) -> List[Dict[str, Any]]:
    """Audit current stock levels for a list of products."""
    results = []
    audit_id = f"STOCK-AUDIT-{uuid4().hex[:8]}"

    for pid in product_ids:
        available, qty = await check_stock_availability(pid, 1)
        results.append({
            "product_id": pid,
            "quantity": qty,
            "has_stock": available,
            "audited_at": datetime.utcnow().isoformat(),
        })

    log_info(
        message=f"Stock audit completed for {len(product_ids)} products",
        transaction_id=audit_id,
    )

    log_inventory_change(
        product_id="batch_audit",
        old_quantity=0,
        new_quantity=0,
        reason=f"Audit check for {len(product_ids)} products",
    )

    return results
