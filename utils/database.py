"""
Database operations with async support.

Defines data schemas as Dict structures and provides
CRUD operations for orders, users, and products.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4


_db_lock = asyncio.Lock()


# ── Data Schemas ──
# These Dict schemas define the expected data shape for each entity.

ORDER_SCHEMA: Dict[str, type] = {
    "user_id": str,
    "products": list,
    "total_amount": float,
    "payment_status": str,
    "shipping_address": dict,
    "payment_transaction_id": str,
}

USER_SCHEMA: Dict[str, type] = {
    "id": str,
    "name": str,
    "email": str,
    "age": int,
    "role": str,
    "is_active": bool,
}

PRODUCT_SCHEMA: Dict[str, type] = {
    "id": str,
    "name": str,
    "price": float,
    "category": str,
    "stock_quantity": int,
    "is_active": bool,
}


def validate_against_schema(
    data: Dict[str, Any], schema: Dict[str, type]
) -> List[str]:
    """Validate a data dict against a schema definition."""
    errors = []
    for field, expected_type in schema.items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"Field '{field}' expected {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )
    return errors


async def save_order(order_data: Dict[str, Any]) -> str:
    """Save an order to the database after schema validation."""
    errors = validate_against_schema(order_data, ORDER_SCHEMA)
    if errors:
        raise ValueError(f"Invalid order data: {'; '.join(errors)}")

    async with _db_lock:
        order_id = f"ORD-{uuid4().hex[:10].upper()}"
        order_data["id"] = order_id
        order_data["created_at"] = datetime.utcnow().isoformat()
        # In production: await db.orders.insert_one(order_data)
        return order_id


async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve user by ID."""
    # In production: return await db.users.find_one({"id": user_id})
    return None


async def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve product by ID."""
    # In production: return await db.products.find_one({"id": product_id})
    return None


async def update_inventory(product_id: str, quantity_change: int) -> bool:
    """Update product inventory with concurrency safety."""
    async with _db_lock:
        product = await get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product not found: {product_id}")
        new_qty = product.get("stock_quantity", 0) + quantity_change
        if new_qty < 0:
            raise ValueError(f"Insufficient stock for product {product_id}")
        # In production: await db.products.update_one(...)
        return True


async def update_order_status(order_id: str, status: str) -> bool:
    """Update the status of an order."""
    valid_statuses = [
        "pending", "processing", "paid",
        "shipped", "delivered", "cancelled",
    ]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}")
    # In production: await db.orders.update_one(...)
    return True
