"""
Tax calculation utilities.

Included in the PR alongside api/billing.py.
Uses TAX_RATE from config/settings.py (main branch).

The pipeline should validate the data flow chain:
  billing.py → tax.py → config/settings.py
  billing.py → database.py (ORDER_SCHEMA)
"""

from typing import Dict, Any

from config.settings import TAX_RATE


# State-level tax overrides (some states have different rates)
STATE_TAX_RATES = {
    "CA": 0.0725,
    "NY": 0.08,
    "TX": 0.0625,
    "FL": 0.06,
    "WA": 0.065,
    "OR": 0.00,
    "DE": 0.00,
    "NH": 0.00,
    "MT": 0.00,
}


def calculate_tax(
    subtotal: float, shipping_address: Dict[str, str]
) -> float:
    """
    Calculate tax amount based on shipping address.

    Uses state-specific rates where available, falls back to
    the global TAX_RATE from config/settings.py.
    """
    if subtotal <= 0:
        return 0.0

    state = shipping_address.get("state", "").upper()
    rate = STATE_TAX_RATES.get(state, TAX_RATE)

    return round(subtotal * rate, 2)


def get_tax_breakdown(
    subtotal: float, shipping_address: Dict[str, str]
) -> Dict[str, Any]:
    """
    Get detailed tax breakdown with rate source.

    Returns the rate used, whether it's state-specific or default,
    and the calculated amount.
    """
    state = shipping_address.get("state", "").upper()

    if state in STATE_TAX_RATES:
        rate = STATE_TAX_RATES[state]
        source = f"state_rate_{state}"
    else:
        rate = TAX_RATE
        source = "default_config"

    return {
        "rate": rate,
        "source": source,
        "state": state or "UNKNOWN",
        "amount": round(subtotal * rate, 2),
        "subtotal": subtotal,
    }
