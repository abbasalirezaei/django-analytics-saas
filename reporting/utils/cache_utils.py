from django.core.cache import cache
from django_redis import get_redis_connection
from django.core.cache import caches

CACHE_TIMEOUT = 300  # Cache timeout in seconds
CACHE_VERSION = "v1"  # Versioning for cache keys


def get_or_set_cache(key, fetch_function, timeout=CACHE_TIMEOUT):
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
    def _make_key(prefix, *parts):
        """
        Internal helper to build structured cache keys with versioning
        """
        joined = ":".join(str(p) for p in parts if p is not None)
        return f"{CACHE_VERSION}:{prefix}:{joined}"

    @staticmethod
    def get_overview_stats(organization_id, website_id, days):
        """Get cached overview stats"""
        key = AnalyticsCache._make_key("analytics_overview", organization_id, website_id, days)
        return cache.get(key)

    @staticmethod
    def set_overview_stats(organization_id, website_id, days, data):
        """Set cached overview stats"""
        key = AnalyticsCache._make_key("analytics_overview", organization_id, website_id, days)
        cache.set(key, data, CACHE_TIMEOUT)

    @staticmethod
    def get_time_series(organization_id, website_id, days):
        """Get cached time series data"""
        key = AnalyticsCache._make_key("analytics_timeseries", organization_id, website_id, days)
        return cache.get(key)

    @staticmethod
    def set_time_series(organization_id, website_id, days, data):
        """Set cached time series data"""
        key = AnalyticsCache._make_key("analytics_timeseries", organization_id, website_id, days)
        cache.set(key, data, CACHE_TIMEOUT)

    @staticmethod
    def get_top_pages(organization_id, website_id, days, limit):
        """Get cached top pages data"""
        key = AnalyticsCache._make_key("analytics_toppages", organization_id, website_id, days, limit)
        return cache.get(key)

    @staticmethod
    def set_top_pages(organization_id, website_id, days, limit, data):
        """Set cached top pages data"""
        key = AnalyticsCache._make_key("analytics_toppages", organization_id, website_id, days, limit)
        cache.set(key, data, CACHE_TIMEOUT)

    @staticmethod
    def invalidate_organization_cache(organization_id):
        """
        Invalidate all cache entries for an organization using pattern matching (Redis only).
        """
        pattern = f"{CACHE_VERSION}:analytics_*:{organization_id}:*"
        try:
            cache_backend = caches['default']
            if hasattr(cache_backend, 'delete_pattern'):
                cache_backend.delete_pattern(pattern)
        except Exception as e:
            print(f"Cache invalidation failed: {e}")
