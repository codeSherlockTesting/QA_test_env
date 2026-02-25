"""
Product model for e-commerce catalog.
"""

from enum import Enum
from typing import Dict, Any, Optional

from models.base import BaseModel
from config.settings import LOW_STOCK_THRESHOLD


class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"


class Product(BaseModel):
    """Product with inventory tracking and category management."""

    def __init__(
        self,
        name: str,
        price: float,
        category: ProductCategory,
        stock_quantity: int = 0,
        seller_id: Optional[str] = None,
        description: str = "",
        **kwargs,
    ):
        super().__init__(kwargs.get("id"))

        if not name or len(name.strip()) < 2:
            raise ValueError("Product name must be at least 2 characters")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")

        self.name = name.strip()
        self.price = round(price, 2)
        self.category = category
        self.stock_quantity = stock_quantity
        self.seller_id = seller_id
        self.description = description
        self.is_active = True

    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0 and self.is_active

    def is_low_stock(self) -> bool:
        return 0 < self.stock_quantity <= LOW_STOCK_THRESHOLD

    def update_stock(self, quantity_change: int):
        new_qty = self.stock_quantity + quantity_change
        if new_qty < 0:
            raise ValueError(
                f"Insufficient stock. Current: {self.stock_quantity}, "
                f"Change: {quantity_change}"
            )
        self.stock_quantity = new_qty
        self.touch()

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "name": self.name,
                "price": self.price,
                "category": self.category.value,
                "stock_quantity": self.stock_quantity,
                "seller_id": self.seller_id,
                "description": self.description,
                "is_active": self.is_active,
            }
        )
        return base
