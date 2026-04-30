"""
Review notification — sends alerts on new reviews.
Imports from reviews.models, reviews.formatter.
"""

import asyncio
from typing import Dict, Any, List

from reviews.models import Review
from reviews.formatter import ReviewFormatter


class ReviewNotifier:
    """Sends notifications when reviews are created or moderated."""

    def __init__(self):
        self._subscribers: Dict[str, List[str]] = {}

    def subscribe(self, product_id: str, callback_url: str):
        if product_id not in self._subscribers:
            self._subscribers[product_id] = []
        self._subscribers[product_id].append(callback_url)

    def unsubscribe(self, product_id: str, callback_url: str):
        if product_id in self._subscribers:
            self._subscribers[product_id] = [
                url for url in self._subscribers[product_id]
                if url != callback_url
            ]

    async def notify_new_review(self, review: Review):
        """Notify subscribers about a new review."""
        formatted = ReviewFormatter.format_review(review)
        subscribers = self._subscribers.get(review.product_id, [])

        for url in subscribers:
            # In production: HTTP POST to callback_url
            await asyncio.sleep(0.01)

        return {"notified": len(subscribers), "product_id": review.product_id}

    async def notify_moderation_result(
        self, review: Review, result: str
    ) -> Dict[str, Any]:
        return {
            "review_id": review.review_id,
            "moderation_result": result,
            "notified": len(self._subscribers.get(review.product_id, [])),
        }
