from django.conf import settings
from django.core.cache import cache


def get_cache_key(prefix, organization_id, website_id=None, date=None):
    """Generate consistent cache keys"""
    key = f"{prefix}:org:{organization_id}"
    if website_id:
        key += f":website:{website_id}"
    if date:
        key += f":date:{date}"
    return key


class AnalyticsCache:
    """Cache manager for analytics data"""

    @staticmethod
    def get_overview_stats(organization_id, website_id, days):
        cache_key = get_cache_key("overview", organization_id, website_id, f"{days}d")
        return cache.get(cache_key)

    @staticmethod
    def set_overview_stats(organization_id, website_id, days, data):
        cache_key = get_cache_key("overview", organization_id, website_id, f"{days}d")
        cache.set(cache_key, data, timeout=settings.CACHE_TTL)

    @staticmethod
    def get_time_series(organization_id, website_id, days):
        cache_key = get_cache_key("timeseries", organization_id, website_id, f"{days}d")
        return cache.get(cache_key)

    @staticmethod
    def set_time_series(organization_id, website_id, days, data):
        cache_key = get_cache_key("timeseries", organization_id, website_id, f"{days}d")
        cache.set(cache_key, data, timeout=settings.CACHE_TTL)

    @staticmethod
    def get_top_pages(organization_id, website_id, days, limit):
        cache_key = get_cache_key(
            f"toppages:limit:{limit}", organization_id, website_id, f"{days}d"
        )
        return cache.get(cache_key)

    @staticmethod
    def set_top_pages(organization_id, website_id, days, limit, data):
        cache_key = get_cache_key(
            f"toppages:limit:{limit}", organization_id, website_id, f"{days}d"
        )
        cache.set(cache_key, data, timeout=settings.CACHE_TTL)

    @staticmethod
    def invalidate_organization_cache(organization_id):
        """Invalidate all cache for an organization"""
        pattern = f"analytics:*:org:{organization_id}:*"
        cache.delete_pattern(pattern)

    @staticmethod
    def invalidate_website_cache(website_id, organization_id):
        """Invalidate cache for specific website"""
        pattern = f"analytics:*:org:{organization_id}:website:{website_id}:*"
        cache.delete_pattern(pattern)
