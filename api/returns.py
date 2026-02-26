"""
Returns API — handles product return and refund requests.

Processes return eligibility checks, inventory release,
refund calculations, and order status updates.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.refund_calculator import RefundCalculator, RefundError
from services.inventory_service import release_stock, check_stock_availability
from utils.logger import log_info, log_error, log_transaction
from utils.database import update_order_status, get_user_by_id


class ReturnError(Exception):
    pass


async def process_return(
    order_id: str,
    user_id: str,
    items_to_return: List[Dict[str, Any]],
    reason: str,
) -> Dict[str, Any]:
    """
    Process a return request for an order.

    Calculates the refund, releases inventory reservations,
    and updates the order status to refunded.
    """
    return_id = f"RET-{uuid4().hex[:8].upper()}"

    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise ReturnError(f"User not found: {user_id}")

        if not items_to_return:
            raise ReturnError("No items specified for return")

        calculator = RefundCalculator()
        refund_amount = calculator.calculate_refund(items_to_return)

        if refund_amount <= 0:
            raise ReturnError("Calculated refund amount is zero or negative")

        released_reservations = []
        for item in items_to_return:
            reservation_id = item.get("reservation_id")
            if reservation_id:
                success = await release_stock(reservation_id=reservation_id)
                if success:
                    released_reservations.append(reservation_id)

        await update_order_status(order_id, "refunded")

        log_transaction(
            transaction_id=return_id,
            amount=refund_amount,
            status="refunded",
            user_id=user_id,
            payment_method="original",
        )

        log_info(
            message=f"Return {return_id} processed for order {order_id}",
            transaction_id=return_id,
            extra={
                "order_id": order_id,
                "refund_amount": refund_amount,
                "items_returned": len(items_to_return),
                "reservations_released": len(released_reservations),
            },
        )

        return {
            "return_id": return_id,
            "order_id": order_id,
            "refund_amount": refund_amount,
            "status": "approved",
            "released_reservations": released_reservations,
            "processed_at": datetime.utcnow().isoformat(),
        }

    except (ReturnError, RefundError):
        raise
    except Exception as e:
        log_error(
            error_message=f"Return processing failed: {str(e)}",
            error_type="ReturnError",
            transaction_id=return_id,
        )
        raise ReturnError(f"Return failed: {str(e)}")


async def get_return_eligibility(
    order_id: str,
    items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Check which items in an order are eligible for return.

    Returns eligible and ineligible item lists with reasons,
    and a total estimated refund for eligible items.
    """
    calculator = RefundCalculator()
    eligible = []
    ineligible = []

    for item in items:
        is_eligible, reason_text = calculator.check_eligibility(item)
        if is_eligible:
            eligible.append(item)
        else:
            ineligible.append({**item, "reason": reason_text})

    estimated_refund = calculator.calculate_refund(eligible)

    return {
        "order_id": order_id,
        "eligible_items": eligible,
        "ineligible_items": ineligible,
        "estimated_refund": estimated_refund,
        "eligible_count": len(eligible),
        "ineligible_count": len(ineligible),
    }


async def get_refund_status(
    return_id: str,
    user_id: str,
) -> Dict[str, Any]:
    """Get the current status of a return request."""
    user = await get_user_by_id(user_id)
    if not user:
        raise ReturnError(f"User not found: {user_id}")

    return {
        "return_id": return_id,
        "user_id": user_id,
        "status": "processing",
        "queried_at": datetime.utcnow().isoformat(),
    }
