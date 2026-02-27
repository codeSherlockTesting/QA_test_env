"""
Session Audit API — security and compliance event recorder.

Tracks user session lifecycle events including login attempts,
token validations, permission checks, and inventory access.
Records form the audit trail required for security monitoring
and regulatory compliance reporting.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.logger import log_info, log_error, log_warning, log_inventory_change
from utils.database import get_user_by_id, get_product_by_id
from services.inventory_service import check_stock_availability


class SessionAuditError(Exception):
    pass


_audit_trail: List[Dict[str, Any]] = []


async def record_login_attempt(
    user_id: str,
    ip_address: str,
    success: bool,
    failure_reason: Optional[str] = None,
) -> Dict[str, Any]:
    """Record a login attempt for security monitoring."""
    audit_id = f"AUTH-{uuid4().hex[:8]}"

    user_data = await get_user_by_id(user_id)

    if success:
        log_info(
            message=f"Successful login: user={user_id} ip={ip_address}",
            transaction_id=audit_id,
        )
    else:
        log_warning(
            message=f"Failed login: user={user_id} ip={ip_address} reason={failure_reason}",
            transaction_id=audit_id,
        )

    event = {
        "audit_id": audit_id,
        "event_type": "login_attempt",
        "user_id": user_id,
        "ip_address": ip_address,
        "success": success,
        "failure_reason": failure_reason,
        "user_role": user_data.get("role") if user_data else None,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    _audit_trail.append(event)
    return event


async def record_token_validation(
    token_id: str,
    user_id: str,
    valid: bool,
    endpoint: Optional[str] = None,
) -> Dict[str, Any]:
    """Record a token validation check for access control auditing."""
    audit_id = f"TOKEN-{uuid4().hex[:8]}"

    if valid:
        log_info(
            message=f"Token validated: token={token_id} user={user_id}",
            transaction_id=audit_id,
        )
    else:
        log_error(
            error_message=f"Token rejected: token={token_id} user={user_id}",
            error_type="TokenValidationError",
            transaction_id=audit_id,
        )

    event = {
        "audit_id": audit_id,
        "event_type": "token_validation",
        "token_id": token_id,
        "user_id": user_id,
        "valid": valid,
        "endpoint": endpoint,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    _audit_trail.append(event)
    return event


async def record_permission_check(
    user_id: str,
    resource: str,
    action: str,
    granted: bool,
) -> Dict[str, Any]:
    """Record a permission evaluation for compliance reporting."""
    audit_id = f"PERM-{uuid4().hex[:8]}"

    outcome = "granted" if granted else "denied"

    log_info(
        message=f"Permission {outcome}: user={user_id} {action}:{resource}",
        transaction_id=audit_id,
    )

    event = {
        "audit_id": audit_id,
        "event_type": "permission_check",
        "user_id": user_id,
        "resource": resource,
        "action": action,
        "granted": granted,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    _audit_trail.append(event)
    return event


async def record_inventory_access(
    user_id: str,
    product_id: str,
    action: str,
) -> Dict[str, Any]:
    """Record inventory data access for warehouse compliance audit."""
    audit_id = f"INV-{uuid4().hex[:8]}"

    product_data = await get_product_by_id(product_id)
    if not product_data:
        raise SessionAuditError(f"Product not found: {product_id}")

    available, current_qty = await check_stock_availability(product_id, 1)

    log_inventory_change(
        product_id=product_id,
        old_quantity=current_qty,
        new_quantity=current_qty,
        reason=f"compliance_audit:{action}",
    )

    log_info(
        message=f"Inventory access: user={user_id} product={product_id} action={action}",
        transaction_id=audit_id,
    )

    event = {
        "audit_id": audit_id,
        "event_type": "inventory_access",
        "user_id": user_id,
        "product_id": product_id,
        "action": action,
        "stock_at_access": current_qty,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    _audit_trail.append(event)
    return event


async def record_data_export(
    user_id: str,
    export_type: str,
    record_count: int,
) -> Dict[str, Any]:
    """Record a data export event for GDPR and compliance tracking."""
    audit_id = f"EXPORT-{uuid4().hex[:8]}"

    user_data = await get_user_by_id(user_id)
    if not user_data:
        raise SessionAuditError(f"User not found: {user_id}")

    if user_data.get("role") not in ("admin", "data_officer"):
        log_warning(
            message=f"Data export by non-privileged user: user={user_id} type={export_type}",
            transaction_id=audit_id,
        )

    log_info(
        message=f"Data export: user={user_id} type={export_type} records={record_count}",
        transaction_id=audit_id,
    )

    event = {
        "audit_id": audit_id,
        "event_type": "data_export",
        "user_id": user_id,
        "export_type": export_type,
        "record_count": record_count,
        "user_role": user_data.get("role"),
        "recorded_at": datetime.utcnow().isoformat(),
    }
    _audit_trail.append(event)
    return event


async def get_audit_trail(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Retrieve audit events, optionally filtered by user or event type."""
    events = list(_audit_trail)

    if user_id:
        events = [e for e in events if e.get("user_id") == user_id]
    if event_type:
        events = [e for e in events if e.get("event_type") == event_type]

    events.sort(key=lambda e: e["recorded_at"], reverse=True)
    return events[:limit]
