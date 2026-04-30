"""
Review input validator — self-contained validation logic.
Imports only from reviews.models.
"""

import re
from typing import Tuple, Dict, Any

from reviews.models import ReviewRating


PROFANITY_LIST = ["spam", "fake", "scam"]
MAX_TITLE_LENGTH = 200
MAX_BODY_LENGTH = 5000
MIN_BODY_LENGTH = 10


class ReviewValidator:
    """Validates review input data."""

    def validate_review_input(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate all fields of a review submission."""
        if not data.get("product_id"):
            return False, "Product ID is required"

        if not data.get("user_id"):
            return False, "User ID is required"

        rating = data.get("rating")
        if not rating or rating not in range(1, 6):
            return False, "Rating must be between 1 and 5"

        title = data.get("title", "")
        ok, err = self._validate_title(title)
        if not ok:
            return False, err

        body = data.get("body", "")
        ok, err = self._validate_body(body)
        if not ok:
            return False, err

        return True, ""

    def _validate_title(self, title: str) -> Tuple[bool, str]:
        if not title or len(title.strip()) < 3:
            return False, "Title must be at least 3 characters"
        if len(title) > MAX_TITLE_LENGTH:
            return False, f"Title exceeds {MAX_TITLE_LENGTH} characters"
        if self._contains_profanity(title):
            return False, "Title contains prohibited content"
        return True, ""

    def _validate_body(self, body: str) -> Tuple[bool, str]:
        if not body or len(body.strip()) < MIN_BODY_LENGTH:
            return False, f"Body must be at least {MIN_BODY_LENGTH} characters"
        if len(body) > MAX_BODY_LENGTH:
            return False, f"Body exceeds {MAX_BODY_LENGTH} characters"
        if self._contains_profanity(body):
            return False, "Body contains prohibited content"
        return True, ""

    def _contains_profanity(self, text: str) -> bool:
        lower = text.lower()
        return any(word in lower for word in PROFANITY_LIST)
