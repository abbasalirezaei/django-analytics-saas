import pytest
from django.core.cache import cache
from reporting.utils.cache_utils import AnalyticsCache

@pytest.mark.django_db
def test_overview_stats_cache():
    org_id = 1
    website_id = 42
    days = 7
    test_data = {"total_pageviews": 100, "cached": True}

    cache.delete_pattern(f"v1:analytics_overview:{org_id}:{website_id}:{days}")
    assert AnalyticsCache.get_overview_stats(org_id, website_id, days) is None

    AnalyticsCache.set_overview_stats(org_id, website_id, days, test_data)
    cached = AnalyticsCache.get_overview_stats(org_id, website_id, days)
    assert cached == test_data

    AnalyticsCache.invalidate_organization_cache(org_id)
    assert AnalyticsCache.get_overview_stats(org_id, website_id, days) is None