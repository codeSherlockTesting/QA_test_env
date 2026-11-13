"""
Review repository — in-memory storage for reviews.
Self-contained, imports only from reviews.models.
"""

import asyncio
from typing import Dict, Any, List, Optional

from reviews.models import Review, ReviewRating


class ReviewRepository:
    """In-memory review storage with async interface."""

    def __init__(self):
        self._reviews: Dict[str, Review] = {}
        self._lock = asyncio.Lock()

    async def save(self, review: Review) -> str:
        async with self._lock:
            self._reviews[review.review_id] = review
            return review.review_id

    async def get_by_id(self, review_id: str) -> Optional[Review]:
        return self._reviews.get(review_id)

    async def get_by_product(self, product_id: str) -> List[Review]:
        return [
            r for r in self._reviews.values()
            if r.product_id == product_id
        ]

    async def get_by_user(self, user_id: str) -> List[Review]:
        return [
            r for r in self._reviews.values()
            if r.user_id == user_id
        ]

    async def get_approved(self, product_id: str) -> List[Review]:
        return [
            r for r in self._reviews.values()
            if r.product_id == product_id and r.is_approved
        ]

    async def get_flagged(self) -> List[Review]:
        return [r for r in self._reviews.values() if r.is_flagged]

    async def delete(self, review_id: str) -> bool:
        async with self._lock:
            return self._reviews.pop(review_id, None) is not None

    async def count(self) -> int:
        return len(self._reviews)
