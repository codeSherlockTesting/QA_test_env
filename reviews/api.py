"""
Review API endpoints — self-contained.
Imports from reviews.service, reviews.formatter.
"""

from typing import Dict, Any, List, Optional

from reviews.service import ReviewService
from reviews.formatter import ReviewFormatter


_service = ReviewService()
_formatter = ReviewFormatter()


async def create_review(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new product review."""
    result = await _service.submit_review(data)
    return {"status": "created", "review": result}


async def get_product_reviews(
    product_id: str, approved_only: bool = True
) -> Dict[str, Any]:
    """Get reviews for a product."""
    reviews = await _service.get_product_reviews(product_id, approved_only)
    stats = await _service.get_stats(product_id)
    return {
        "product_id": product_id,
        "stats": stats,
        "reviews": reviews,
    }


async def approve_review(review_id: str) -> Dict[str, Any]:
    await _service.approve_review(review_id)
    return {"status": "approved", "review_id": review_id}


async def delete_review(review_id: str) -> Dict[str, Any]:
    deleted = await _service.delete_review(review_id)
    return {"status": "deleted" if deleted else "not_found"}


async def vote_helpful(review_id: str) -> Dict[str, Any]:
    review = await _service.repo.get_by_id(review_id)
    if not review:
        raise ValueError(f"Review not found: {review_id}")
    review.mark_helpful()
    return {"review_id": review_id, "helpful_votes": review.helpful_votes}
