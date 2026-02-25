"""
Reports API — generates sales reports.

This file imports from utils/report_helper.py (also in this PR),
but the import path is INTENTIONALLY TYPOED:
  "from utils.report_hepler import ..."  (note: "hepler" not "helper")

The pipeline should:
1. Try to resolve the typoed import
2. NOT silently fail or provide shallow analysis
3. Report an "Import Error" or "Module Not Found" warning
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import uuid4

from utils.logger import log_info, log_error

# BUG: Typoed import path — "report_hepler" instead of "report_helper"
from utils.report_hepler import (
    aggregate_sales,
    format_report_output,
    ReportTimeRange,
)


class ReportGenerationError(Exception):
    pass


async def generate_sales_report(
    start_date: str,
    end_date: str,
    group_by: str = "day",
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a sales report for the given date range.

    Args:
        start_date: Report start date (YYYY-MM-DD)
        end_date: Report end date (YYYY-MM-DD)
        group_by: Aggregation level (day, week, month)
        category: Optional product category filter

    Returns:
        Dict with report data, totals, and metadata
    """
    report_id = f"RPT-{uuid4().hex[:8].upper()}"

    try:
        log_info(
            message=f"Generating report {report_id}: {start_date} to {end_date}",
            transaction_id=report_id,
        )

        time_range = ReportTimeRange(
            start=start_date,
            end=end_date,
            granularity=group_by,
        )

        raw_data = await aggregate_sales(
            time_range=time_range,
            category_filter=category,
        )

        formatted = format_report_output(
            data=raw_data,
            report_id=report_id,
            generated_at=datetime.utcnow().isoformat(),
        )

        log_info(
            message=f"Report {report_id} generated: {len(raw_data)} records",
            transaction_id=report_id,
            extra={"group_by": group_by, "category": category},
        )

        return formatted

    except Exception as e:
        log_error(
            error_message=f"Report generation failed: {str(e)}",
            error_type="ReportGenerationError",
            transaction_id=report_id,
        )
        raise ReportGenerationError(f"Failed to generate report: {str(e)}")
