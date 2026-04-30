"""
Review analytics — trends and insights.
Imports from reviews.models, reviews.repository, reviews.aggregator.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

from reviews.models import Review
from reviews.repository import ReviewRepository
from reviews.aggregator import ReviewAggregator


class ReviewAnalytics:
    """Generate review analytics and trend reports."""

    def __init__(self, repo: ReviewRepository):
        self.repo = repo
        self.aggregator = ReviewAggregator(repo)

    async def get_sentiment_trend(
        self, product_id: str, days: int = 30
    ) -> List[Dict[str, Any]]:
        reviews = await self.repo.get_by_product(product_id)
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent = [r for r in reviews if r.created_at >= cutoff]

        daily = {}
        for r in recent:
            day = r.created_at.strftime("%Y-%m-%d")
            if day not in daily:
                daily[day] = {"ratings": [], "count": 0}
            daily[day]["ratings"].append(r.rating.value)
            daily[day]["count"] += 1

        trend = []
        for day, data in sorted(daily.items()):
            avg = sum(data["ratings"]) / len(data["ratings"])
            trend.append({"date": day, "avg_rating": round(avg, 2), "count": data["count"]})

        return trend

    async def get_top_reviewers(self, limit: int = 10) -> List[Dict[str, Any]]:
        all_reviews = list((await self.repo.get_flagged()) or [])
        user_counts: Dict[str, int] = {}
        for r in all_reviews:
            user_counts[r.user_id] = user_counts.get(r.user_id, 0) + 1

        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
        return [
            {"user_id": uid, "review_count": count}
            for uid, count in sorted_users[:limit]
        ]
