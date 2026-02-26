"""
Wishlist validation utilities.

Validates wishlist operations including size limits, duplicate
entries, and product availability eligibility checks.
"""

from typing import Dict, Any, List, Tuple

from models.product import Product, ProductCategory


MAX_WISHLIST_ITEMS = 100


class WishlistValidationError(Exception):
    pass


class WishlistValidator:
    """Validates wishlist add/remove operations."""

    def validate_add(
        self,
        user_id: str,
        product_id: str,
        wishlists: Dict[str, List],
    ) -> None:
        """
        Validate that a product can be added.

        Checks wishlist size limit and duplicate entries.
        """
        user_items = wishlists.get(user_id, [])

        if len(user_items) >= MAX_WISHLIST_ITEMS:
            raise WishlistValidationError(
                f"Wishlist is full. Maximum {MAX_WISHLIST_ITEMS} items allowed."
            )

        already_saved = any(
            i["product_id"] == product_id for i in user_items
        )
        if already_saved:
            raise WishlistValidationError(
                f"Product {product_id} is already in the wishlist."
            )

    def validate_product_eligibility(
        self, product: Product
    ) -> Tuple[bool, str]:
        """Check if a product is eligible for wishlisting."""
        if not product.is_active:
            return False, f"Product '{product.name}' is not currently available"
        return True, ""
