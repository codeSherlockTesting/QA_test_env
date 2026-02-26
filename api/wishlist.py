"""
Wishlist API — customer product wishlists.

Allows customers to save and monitor products for future purchase.
Provides live stock status and low-stock alerts on wishlist items.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.wishlist_validator import WishlistValidator, WishlistValidationError
from models.product import Product, ProductCategory
from utils.database import get_product_by_id, get_user_by_id
from utils.logger import log_info, log_error


class WishlistError(Exception):
    pass


_wishlists: Dict[str, List[Dict]] = {}


async def add_to_wishlist(user_id: str, product_id: str) -> Dict[str, Any]:
    """
    Add a product to the user's wishlist.

    Validates the user and product exist, checks wishlist limits,
    and records the current stock status at the time of saving.
    """
    txn_id = f"WL-ADD-{uuid4().hex[:8]}"

    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise WishlistError(f"User not found: {user_id}")

        product_data = await get_product_by_id(product_id)
        if not product_data:
            raise WishlistError(f"Product not found: {product_id}")

        product = Product(
            name=product_data["name"],
            price=product_data["price"],
            category=ProductCategory(product_data["category"]),
            stock_quantity=product_data.get("stock_quantity", 0),
            id=product_data.get("id"),
        )

        validator = WishlistValidator()
        validator.validate_add(user_id, product_id, _wishlists)

        item = {
            "product_id": product_id,
            "product_name": product_data["name"],
            "price": product_data["price"],
            "in_stock": product.is_in_stock(),
            "low_stock": product.is_low_stock(),
            "added_at": datetime.utcnow().isoformat(),
        }

        if user_id not in _wishlists:
            _wishlists[user_id] = []
        _wishlists[user_id].append(item)

        log_info(
            message=f"Product {product_id} added to wishlist for {user_id}",
            transaction_id=txn_id,
            extra={"user_id": user_id, "product_id": product_id},
        )

        return {"status": "added", "item": item}

    except (WishlistValidationError, WishlistError):
        raise
    except Exception as e:
        log_error(
            error_message=f"Wishlist add failed: {str(e)}",
            error_type="WishlistError",
            transaction_id=txn_id,
        )
        raise WishlistError(str(e))


async def get_wishlist(user_id: str) -> Dict[str, Any]:
    """
    Retrieve the user's wishlist with refreshed live stock status.

    Re-fetches product data for every item so in_stock and
    low_stock reflect the current warehouse state.
    """
    txn_id = f"WL-GET-{uuid4().hex[:8]}"
    saved_items = _wishlists.get(user_id, [])

    refreshed = []
    for item in saved_items:
        product_data = await get_product_by_id(item["product_id"])
        if product_data:
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                category=ProductCategory(product_data["category"]),
                stock_quantity=product_data.get("stock_quantity", 0),
            )
            refreshed.append({
                **item,
                "in_stock": product.is_in_stock(),
                "low_stock": product.is_low_stock(),
                "current_price": product_data["price"],
            })
        else:
            refreshed.append({**item, "in_stock": False, "low_stock": False})

    log_info(
        message=f"Wishlist retrieved for {user_id}: {len(refreshed)} items",
        transaction_id=txn_id,
    )

    return {
        "user_id": user_id,
        "items": refreshed,
        "total_items": len(refreshed),
        "in_stock_count": sum(1 for i in refreshed if i.get("in_stock")),
        "low_stock_count": sum(1 for i in refreshed if i.get("low_stock")),
    }


async def remove_from_wishlist(user_id: str, product_id: str) -> Dict[str, Any]:
    """Remove a product from the user's wishlist."""
    if user_id not in _wishlists:
        raise WishlistError(f"No wishlist found for user: {user_id}")

    original_count = len(_wishlists[user_id])
    _wishlists[user_id] = [
        i for i in _wishlists[user_id] if i["product_id"] != product_id
    ]

    if len(_wishlists[user_id]) == original_count:
        raise WishlistError(f"Product {product_id} is not in the wishlist")

    return {"status": "removed", "product_id": product_id}


async def get_low_stock_alerts(user_id: str) -> List[Dict[str, Any]]:
    """Return wishlist items that are running low on stock."""
    saved_items = _wishlists.get(user_id, [])
    alerts = []

    for item in saved_items:
        product_data = await get_product_by_id(item["product_id"])
        if product_data:
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                category=ProductCategory(product_data["category"]),
                stock_quantity=product_data.get("stock_quantity", 0),
            )
            if product.is_low_stock():
                alerts.append({
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "stock_quantity": product_data.get("stock_quantity"),
                    "price": product_data["price"],
                })

    return alerts
