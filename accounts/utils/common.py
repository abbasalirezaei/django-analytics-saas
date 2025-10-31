"""
Common utility functions for the accounts module.
"""
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for list views
    """

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


def get_cached_data(key: str, timeout: int = 3600) -> Optional[Any]:
    """
    Get data from cache with standard prefix
    """
    return cache.get(f"{settings.CACHE_PREFIX}:{key}")


def set_cached_data(key: str, value: Any, timeout: int = 3600) -> None:
    """
    Set data in cache with standard prefix
    """
    cache.set(f"{settings.CACHE_PREFIX}:{key}", value, timeout=timeout)


def validate_input(data: Dict[str, Any], required_fields: list) -> tuple[bool, list]:
    """
    Validate input data against required fields
    Returns: (is_valid, error_messages)
    """
    errors = []
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not data[field]:
            errors.append(f"Field cannot be empty: {field}")

    return len(errors) == 0, errors
