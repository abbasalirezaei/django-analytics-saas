"""
Common utility functions for reporting
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_date_range(start_date: str, end_date: str) -> Tuple[datetime, datetime]:
    """
    Validate and parse date range parameters
    """
    try:
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            start = timezone.now().date() - timedelta(days=7)

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            end = timezone.now().date()

        if start > end:
            raise ValidationError("Start date cannot be after end date")

        if (end - start).days > 365:
            raise ValidationError("Date range cannot exceed 365 days")

        return start, end

    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD")


def format_analytics_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format analytics data for consistent output
    """
    formatted_data = {}

    for key, value in data.items():
        if isinstance(value, float):
            # Round floats to 2 decimal places
            formatted_data[key] = round(value, 2)
        elif hasattr(value, "isoformat"):
            # Convert datetime objects to ISO format
            formatted_data[key] = value.isoformat()
        else:
            formatted_data[key] = value

    return formatted_data


def get_period_label(days: int) -> str:
    """
    Get human-readable period label
    """
    if days == 1:
        return "Today"
    elif days == 7:
        return "Last 7 days"
    elif days == 30:
        return "Last 30 days"
    elif days == 90:
        return "Last 90 days"
    else:
        return f"Last {days} days"


def calculate_growth_rate(current: float, previous: float) -> float:
    """
    Calculate growth rate percentage
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round(((current - previous) / previous) * 100, 2)


def get_default_filters(organization, website_id: int = None) -> Dict[str, Any]:
    """
    Get default filters for analytics queries
    """
    filters = {"website__organization": organization}
    if website_id:
        filters["website_id"] = website_id
    return filters
