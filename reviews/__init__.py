"""
Self-contained product reviews module.

All files in this package import ONLY from each other.
No dependencies on the main branch. This tests that the
new pipeline performs as well as the old one when no
fetching is required.
"""

from reviews.models import Review, ReviewRating, ReviewStats
from reviews.repository import ReviewRepository
from reviews.service import ReviewService
from reviews.validator import ReviewValidator
from reviews.aggregator import ReviewAggregator
from reviews.formatter import ReviewFormatter
from reviews.api import create_review, get_product_reviews
from reviews.moderation import ReviewModerator
from reviews.analytics import ReviewAnalytics
from reviews.exporter import ReviewExporter
from reviews.notifier import ReviewNotifier
