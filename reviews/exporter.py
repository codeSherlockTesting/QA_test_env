"""
Review exporter — export reviews to various formats.
Imports from reviews.models, reviews.repository, reviews.formatter.
"""

import json
from typing import Dict, Any, List

from reviews.models import Review
from reviews.repository import ReviewRepository
from reviews.formatter import ReviewFormatter


class ReviewExporter:
    """Export reviews to JSON or CSV format."""

    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    async def export_product_reviews(
        self, product_id: str, format: str = "json"
    ) -> str:
        reviews = await self.repo.get_by_product(product_id)

        if format == "json":
            return self._to_json(reviews)
        elif format == "csv":
            return self._to_csv(reviews)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _to_json(self, reviews: List[Review]) -> str:
        data = [ReviewFormatter.format_review(r) for r in reviews]
        return json.dumps({"reviews": data, "count": len(data)}, indent=2)

    def _to_csv(self, reviews: List[Review]) -> str:
        header = "review_id,product_id,rating,title,verified,date\n"
        rows = []
        for r in reviews:
            rows.append(
                f'{r.review_id},{r.product_id},{r.rating.value},'
                f'"{r.title}",{r.verified_purchase},'
                f'{r.created_at.strftime("%Y-%m-%d")}'
            )
        return header + "\n".join(rows)
