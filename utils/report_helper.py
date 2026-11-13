"""
Report helper utilities — provides aggregation and formatting.

NOTE: This file's actual name is "report_helper.py" but the
importing file (api/reports.py) has a typo and imports from
"report_hepler" instead. This should trigger an import error.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ReportTimeRange:
    start: str
    end: str
    granularity: str = "day"

    def validate(self) -> bool:
        try:
            s = datetime.strptime(self.start, "%Y-%m-%d")
            e = datetime.strptime(self.end, "%Y-%m-%d")
            return e >= s and self.granularity in ("day", "week", "month")
        except ValueError:
            return False


async def aggregate_sales(
    time_range: ReportTimeRange,
    category_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Aggregate sales data for the given time range.

    In production, this queries the database.
    """
    if not time_range.validate():
        raise ValueError(f"Invalid time range: {time_range}")

    # Simulated aggregation
    return [
        {
            "date": time_range.start,
            "total_sales": 1500.00,
            "order_count": 12,
            "category": category_filter or "all",
        }
    ]


def format_report_output(
    data: List[Dict[str, Any]],
    report_id: str,
    generated_at: str,
) -> Dict[str, Any]:
    """Format raw aggregated data into a report structure."""
    total_sales = sum(row.get("total_sales", 0) for row in data)
    total_orders = sum(row.get("order_count", 0) for row in data)

    return {
        "report_id": report_id,
        "generated_at": generated_at,
        "summary": {
            "total_sales": round(total_sales, 2),
            "total_orders": total_orders,
            "period_count": len(data),
        },
        "data": data,
    }
