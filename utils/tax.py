"""
Tax calculation utilities for regional invoice pricing.

Applies state-specific tax rates where available, falling back
to the globally configured default rate for unrecognized regions.
"""

from typing import Dict, Any

from config.settings import TAX_RATE


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
    subtotal: float,
    shipping_address: Dict[str, str],
) -> float:
    """
    Calculate the tax amount for a given subtotal and shipping location.

    Uses the state code from the address to apply a state-specific rate.
    Falls back to the global TAX_RATE constant for states not in the table.
    Returns 0.0 for zero or negative subtotals.
    """
    if subtotal <= 0:
        return 0.0

    state = shipping_address.get("state", "").upper()
    rate = STATE_TAX_RATES.get(state, TAX_RATE)

    return round(subtotal * rate, 2)


def get_tax_breakdown(
    subtotal: float,
    shipping_address: Dict[str, str],
) -> Dict[str, Any]:
    """
    Return a detailed breakdown of the tax calculation for an order.

    Indicates whether the rate was pulled from the state table or the
    global config default, along with the final computed amount.
    """
    if subtotal <= 0:
        return {
            "rate": 0.0,
            "source": "zero_subtotal",
            "state": "N/A",
            "amount": 0.0,
            "subtotal": subtotal,
        }

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
