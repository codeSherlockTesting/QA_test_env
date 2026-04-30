"""
Review moderation — auto-moderation and flagging.
Imports from reviews.models, reviews.repository, reviews.validator.
"""

from typing import Dict, Any, List

from reviews.models import Review
from reviews.repository import ReviewRepository
from reviews.validator import ReviewValidator


class ReviewModerator:
    """Handles review moderation — auto-approve and flagging."""

    def __init__(self, repo: ReviewRepository):
        self.repo = repo
        self.validator = ReviewValidator()

    async def auto_moderate(self, review: Review) -> str:
        """Auto-moderate a review. Returns 'approved', 'flagged', or 'pending'."""
        data = review.to_dict()
        is_valid, _ = self.validator.validate_review_input(data)

        if not is_valid:
            review.flag()
            return "flagged"

        if review.verified_purchase and review.rating.value >= 3:
            review.approve()
            return "approved"

        return "pending"

    async def get_moderation_queue(self) -> List[Dict[str, Any]]:
        """Get all reviews pending moderation."""
        flagged = await self.repo.get_flagged()
        return [r.to_dict() for r in flagged]

    async def bulk_approve(self, review_ids: List[str]) -> Dict[str, int]:
        approved = 0
        for rid in review_ids:
            review = await self.repo.get_by_id(rid)
            if review and not review.is_approved:
                review.approve()
                approved += 1
        return {"approved": approved, "total": len(review_ids)}
