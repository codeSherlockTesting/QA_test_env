"""
Review data models — self-contained, no external deps.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from uuid import uuid4


class ReviewRating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Review:
    """Product review model."""

    def __init__(
        self,
        product_id: str,
        user_id: str,
        rating: ReviewRating,
        title: str,
        body: str,
        verified_purchase: bool = False,
    ):
        if not title or len(title) < 3:
            raise ValueError("Review title must be at least 3 characters")
        if not body or len(body) < 10:
            raise ValueError("Review body must be at least 10 characters")

        self.review_id = f"REV-{uuid4().hex[:8]}"
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.title = title.strip()
        self.body = body.strip()
        self.verified_purchase = verified_purchase
        self.created_at = datetime.utcnow()
        self.helpful_votes = 0
        self.is_approved = False
        self.is_flagged = False

    def mark_helpful(self):
        self.helpful_votes += 1

    def approve(self):
        self.is_approved = True

    def flag(self):
        self.is_flagged = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "rating": self.rating.value,
            "title": self.title,
            "body": self.body,
            "verified_purchase": self.verified_purchase,
            "helpful_votes": self.helpful_votes,
            "is_approved": self.is_approved,
            "is_flagged": self.is_flagged,
            "created_at": self.created_at.isoformat(),
        }


class ReviewStats:
    """Aggregated statistics for a product's reviews."""

    def __init__(self, product_id: str):
        self.product_id = product_id
        self.total_reviews = 0
        self.average_rating = 0.0
        self.rating_distribution: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def update(self, reviews: List[Review]):
        self.total_reviews = len(reviews)
        if reviews:
            total = sum(r.rating.value for r in reviews)
            self.average_rating = round(total / len(reviews), 2)
            self.rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for r in reviews:
                self.rating_distribution[r.rating.value] += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "total_reviews": self.total_reviews,
            "average_rating": self.average_rating,
            "rating_distribution": self.rating_distribution,
        }
