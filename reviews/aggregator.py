"""
Review aggregator — computes aggregate metrics.
Imports from reviews.models, reviews.repository.
"""

from typing import Dict, Any, List

from reviews.models import Review, ReviewStats
from reviews.repository import ReviewRepository


class ReviewAggregator:
    """Computes aggregate review metrics across products."""

    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    async def get_top_rated(
        self, product_ids: List[str], min_reviews: int = 3
    ) -> List[Dict[str, Any]]:
        """Get top-rated products from the given list."""
        results = []
        for pid in product_ids:
            reviews = await self.repo.get_approved(pid)
            if len(reviews) >= min_reviews:
                stats = ReviewStats(pid)
                stats.update(reviews)
                results.append(stats.to_dict())

        results.sort(key=lambda x: x["average_rating"], reverse=True)
        return results

    async def get_rating_summary(self, product_id: str) -> Dict[str, Any]:
        reviews = await self.repo.get_by_product(product_id)
        stats = ReviewStats(product_id)
        stats.update(reviews)

        verified = [r for r in reviews if r.verified_purchase]
        verified_stats = ReviewStats(product_id)
        verified_stats.update(verified)

        return {
            "overall": stats.to_dict(),
            "verified_only": verified_stats.to_dict(),
            "verified_percentage": (
                round(len(verified) / len(reviews) * 100, 1) if reviews else 0
            ),
        }
