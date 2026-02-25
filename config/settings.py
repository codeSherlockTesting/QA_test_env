"""
Centralized application configuration for the e-commerce platform.
All constants and environment-specific settings are defined here.
"""

import os


# ── Tax Configuration ──
TAX_RATE = 0.08

# ── Order Limits ──
MAX_ORDER_AMOUNT = 10000.00
MIN_ORDER_AMOUNT = 5.00
MAX_CART_ITEMS = 50

# ── Payment Gateway ──
PAYMENT_GATEWAY_URL = os.getenv(
    "PAYMENT_GATEWAY_URL", "https://api.payments.example.com/v1"
)
PAYMENT_TIMEOUT_SECONDS = 30
MAX_PAYMENT_RETRIES = 3

# ── Database ──
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://localhost:5432/ecommerce"
)
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20

# ── Redis ──
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = 300

# ── Email ──
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.example.com")
EMAIL_SMTP_PORT = 587
EMAIL_FROM_ADDRESS = "noreply@ecommerce.example.com"
EMAIL_USE_TLS = True

# ── Security ──
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
BCRYPT_ROUNDS = 12
MIN_PASSWORD_LENGTH = 8

# ── Inventory ──
LOW_STOCK_THRESHOLD = 10
RESERVATION_TIMEOUT_MINUTES = 15

# ── Logging ──
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "json"
