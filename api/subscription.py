"""
Subscription API — manages recurring order plans.

Allows customers to schedule automated repeat purchases.
Each billing cycle places a new order using the stored
subscription plan without requiring manual re-entry.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.database import save_order, get_user_by_id, get_product_by_id
from config.settings import TAX_RATE
from utils.logger import log_info, log_error, log_warning


class SubscriptionError(Exception):
    pass


_subscriptions: Dict[str, Dict[str, Any]] = {}


async def create_subscription(
    user_id: str,
    subscription_plan: Dict[str, Any],
    billing_interval_days: int = 30,
) -> Dict[str, Any]:
    """
    Create a recurring subscription and place the first order.

    Accepts a subscription plan from the caller, builds the initial
    order, and stores the plan for future billing cycles.
    """
    txn_id = f"SUB-CREATE-{uuid4().hex[:8]}"

    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise SubscriptionError(f"User not found: {user_id}")

        order_data = {
            "user_id": user_id,
            "products": subscription_plan.get("items", []),
            "total_amount": subscription_plan.get("total", 0.0),
            "payment_status": subscription_plan.get("payment_status", "pending"),
            "shipping_address": subscription_plan.get("shipping_address", {}),
            "payment_transaction_id": subscription_plan.get("payment_id", ""),
        }

        order_id = await save_order(order_data)

        subscription_id = f"RSUB-{uuid4().hex[:8]}"
        _subscriptions[subscription_id] = {
            "subscription_id": subscription_id,
            "user_id": user_id,
            "plan": subscription_plan,
            "billing_interval_days": billing_interval_days,
            "initial_order_id": order_id,
            "next_billing_date": (
                datetime.utcnow() + timedelta(days=billing_interval_days)
            ).isoformat(),
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
        }

        log_info(
            message=f"Subscription {subscription_id} created for user {user_id}",
            transaction_id=txn_id,
            extra={"subscription_id": subscription_id, "order_id": order_id},
        )

        return {
            "subscription_id": subscription_id,
            "order_id": order_id,
            "status": "active",
            "next_billing_date": _subscriptions[subscription_id]["next_billing_date"],
        }

    except SubscriptionError:
        raise
    except ValueError as e:
        log_error(
            error_message=f"Subscription creation failed: {str(e)}",
            error_type="ValueError",
            transaction_id=txn_id,
        )
        raise SubscriptionError(str(e))


async def process_billing_cycle(subscription_id: str) -> Dict[str, Any]:
    """
    Execute the next billing cycle for an active subscription.

    Retrieves the stored subscription plan, calculates current
    totals, and places a new order for the billing period.
    """
    txn_id = f"SUB-BILL-{uuid4().hex[:8]}"

    subscription = _subscriptions.get(subscription_id)
    if not subscription:
        raise SubscriptionError(f"Subscription not found: {subscription_id}")

    if subscription.get("status") != "active":
        raise SubscriptionError(
            f"Subscription {subscription_id} is not active"
        )

    plan = subscription["plan"]

    order_data = {
        "user_id": subscription["user_id"],
        "products": plan.get("items", []),
        "total_amount": plan.get("total", 0.0),
        "payment_status": "pending",
        "shipping_address": plan.get("shipping_address", {}),
        "payment_transaction_id": f"CYCLE-{uuid4().hex[:10]}",
    }

    try:
        order_id = await save_order(order_data)

        subscription["next_billing_date"] = (
            datetime.utcnow()
            + timedelta(days=subscription["billing_interval_days"])
        ).isoformat()
        subscription["last_order_id"] = order_id

        log_info(
            message=f"Billing cycle complete for subscription {subscription_id}",
            transaction_id=txn_id,
            extra={"subscription_id": subscription_id, "order_id": order_id},
        )

        return {
            "subscription_id": subscription_id,
            "order_id": order_id,
            "next_billing_date": subscription["next_billing_date"],
        }

    except ValueError as e:
        log_error(
            error_message=f"Billing cycle failed for {subscription_id}: {str(e)}",
            error_type="ValueError",
            transaction_id=txn_id,
        )
        raise SubscriptionError(str(e))


async def pause_subscription(
    subscription_id: str,
    user_id: str,
    resume_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Pause an active subscription until a specified date."""
    txn_id = f"SUB-PAUSE-{uuid4().hex[:8]}"

    subscription = _subscriptions.get(subscription_id)
    if not subscription:
        raise SubscriptionError(f"Subscription not found: {subscription_id}")

    if subscription["user_id"] != user_id:
        raise SubscriptionError("Cannot modify another user's subscription")

    subscription["status"] = "paused"
    subscription["paused_at"] = datetime.utcnow().isoformat()
    if resume_date:
        subscription["resume_date"] = resume_date

    log_info(
        message=f"Subscription {subscription_id} paused by user {user_id}",
        transaction_id=txn_id,
        extra={"resume_date": resume_date},
    )

    return {
        "subscription_id": subscription_id,
        "status": "paused",
        "paused_at": subscription["paused_at"],
        "resume_date": resume_date,
    }


async def cancel_subscription(
    subscription_id: str,
    user_id: str,
) -> Dict[str, Any]:
    """Permanently cancel an active subscription."""
    txn_id = f"SUB-CANCEL-{uuid4().hex[:8]}"

    subscription = _subscriptions.get(subscription_id)
    if not subscription:
        raise SubscriptionError(f"Subscription not found: {subscription_id}")

    if subscription["user_id"] != user_id:
        raise SubscriptionError("Cannot cancel another user's subscription")

    if subscription["status"] == "cancelled":
        log_warning(
            message=f"Subscription {subscription_id} is already cancelled",
            transaction_id=txn_id,
        )
        return {"subscription_id": subscription_id, "status": "cancelled"}

    subscription["status"] = "cancelled"
    subscription["cancelled_at"] = datetime.utcnow().isoformat()

    log_info(
        message=f"Subscription {subscription_id} cancelled by user {user_id}",
        transaction_id=txn_id,
        extra={"subscription_id": subscription_id},
    )

    return {
        "subscription_id": subscription_id,
        "status": "cancelled",
        "cancelled_at": subscription["cancelled_at"],
    }
