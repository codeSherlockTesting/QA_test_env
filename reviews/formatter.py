"""
Review formatter — formats reviews for display.
Imports from reviews.models.
"""

from datetime import datetime
from typing import Dict, Any, List

from reviews.models import Review, ReviewStats


class ReviewFormatter:
    """Formats review data for API responses."""

    @staticmethod
    def format_review(review: Review) -> Dict[str, Any]:
        stars = "*" * review.rating.value
        return {
            "id": review.review_id,
            "stars": stars,
            "title": review.title,
            "body": review.body[:200] + "..." if len(review.body) > 200 else review.body,
            "author": review.user_id,
            "verified": review.verified_purchase,
            "helpful": review.helpful_votes,
            "date": review.created_at.strftime("%B %d, %Y"),
        }

    @staticmethod
    def format_stats_summary(stats: ReviewStats) -> str:
        dist = stats.rating_distribution
        lines = [
            f"Average: {stats.average_rating}/5 ({stats.total_reviews} reviews)",
            "",
        ]
        for star in range(5, 0, -1):
            count = dist.get(star, 0)
            bar = "#" * count
            lines.append(f"  {star} star: {bar} ({count})")
        return "\n".join(lines)

    @staticmethod
    def format_review_list(reviews: List[Review]) -> List[Dict[str, Any]]:
        return [ReviewFormatter.format_review(r) for r in reviews]
