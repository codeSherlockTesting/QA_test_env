"""
Review service — orchestrates review operations.
Imports from reviews.models, reviews.repository, reviews.validator.
"""

from typing import Dict, Any, List, Optional

from reviews.models import Review, ReviewRating, ReviewStats
from reviews.repository import ReviewRepository
from reviews.validator import ReviewValidator


class ReviewService:
    """Business logic layer for reviews."""

    def __init__(self):
        self.repo = ReviewRepository()
        self.validator = ReviewValidator()

    async def submit_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new review after validation."""
        is_valid, error = self.validator.validate_review_input(data)
        if not is_valid:
            raise ValueError(f"Invalid review: {error}")

        existing = await self.repo.get_by_user(data["user_id"])
        already_reviewed = any(
            r.product_id == data["product_id"] for r in existing
        )
        if already_reviewed:
            raise ValueError("User already reviewed this product")

        review = Review(
            product_id=data["product_id"],
            user_id=data["user_id"],
            rating=ReviewRating(data["rating"]),
            title=data["title"],
            body=data["body"],
            verified_purchase=data.get("verified_purchase", False),
        )

        await self.repo.save(review)
        return review.to_dict()

    async def get_product_reviews(
        self, product_id: str, approved_only: bool = True
    ) -> List[Dict[str, Any]]:
        if approved_only:
            reviews = await self.repo.get_approved(product_id)
        else:
            reviews = await self.repo.get_by_product(product_id)
        return [r.to_dict() for r in reviews]

    async def get_stats(self, product_id: str) -> Dict[str, Any]:
        reviews = await self.repo.get_by_product(product_id)
        stats = ReviewStats(product_id)
        stats.update(reviews)
        return stats.to_dict()

    async def approve_review(self, review_id: str) -> bool:
        review = await self.repo.get_by_id(review_id)
        if not review:
            raise ValueError(f"Review not found: {review_id}")
        review.approve()
        return True

    async def delete_review(self, review_id: str) -> bool:
        return await self.repo.delete(review_id)
