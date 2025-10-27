from django.core.cache import cache
from typing import Any, Callable, Optional
from tracking.models import PageView, Session, Event
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta


def get_or_set_cache(key: str, fetch_function: Callable, timeout: int = 300) -> Any:
    """
    Utility function to get data from cache or fetch and set it if not present.

    :param key: Cache key
    :param fetch_function: Function to fetch data if not in cache
    :param timeout: Cache timeout in seconds
    :return: Cached or fetched data
    """
    data = cache.get(key)
    if data is None:
        data = fetch_function()
        cache.set(key, data, timeout)
    return data


class AnalyticsCache:
    """
    Cache utility class for analytics data
    """
    
    @staticmethod
    def get_overview_stats(organization_id: int, website_id: Optional[int], days: int) -> Optional[dict]:
        """Get cached overview stats"""
        cache_key = f"analytics_overview:{organization_id}:{website_id}:{days}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_overview_stats(organization_id: int, website_id: Optional[int], days: int, data: dict) -> None:
        """Set cached overview stats"""
        cache_key = f"analytics_overview:{organization_id}:{website_id}:{days}"
        cache.set(cache_key, data, timeout=300)  # 5 minutes
    
    @staticmethod
    def get_time_series(organization_id: int, website_id: Optional[int], days: int) -> Optional[list]:
        """Get cached time series data"""
        cache_key = f"analytics_timeseries:{organization_id}:{website_id}:{days}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_time_series(organization_id: int, website_id: Optional[int], days: int, data: list) -> None:
        """Set cached time series data"""
        cache_key = f"analytics_timeseries:{organization_id}:{website_id}:{days}"
        cache.set(cache_key, data, timeout=300)  # 5 minutes
    
    @staticmethod
    def get_top_pages(organization_id: int, website_id: Optional[int], days: int, limit: int) -> Optional[list]:
        """Get cached top pages data"""
        cache_key = f"analytics_toppages:{organization_id}:{website_id}:{days}:{limit}"
        return cache.get(cache_key)
    
    @staticmethod
    def set_top_pages(organization_id: int, website_id: Optional[int], days: int, limit: int, data: list) -> None:
        """Set cached top pages data"""
        cache_key = f"analytics_toppages:{organization_id}:{website_id}:{days}:{limit}"
        cache.set(cache_key, data, timeout=300)  # 5 minutes
    
    @staticmethod
    def invalidate_organization_cache(organization_id: int) -> None:
        """Invalidate all cache entries for an organization"""
        # This would need to be implemented based on your cache backend
        # For Redis, you could use pattern matching
        pass