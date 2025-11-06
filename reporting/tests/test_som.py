from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models.organization import Organization
from accounts.models.user import User
from tracking.models import Event, PageView, Session, Website


@pytest.mark.django_db
def test_analytics_overview_authenticated(client, django_user_model):
    # Setup organization, user, website, and some tracking data
    org = Organization.objects.create(name="TestOrg")
    user = django_user_model.objects.create_user(
        username="user1", email="user@test.com", password="pass", organization=org
    )
    website = Website.objects.create(
        name="TestSite", domain="test.com", organization=org
    )
    session = Session.objects.create(
        website=website, session_id="sess1", started_at=timezone.now()
    )
    PageView.objects.create(
        website=website, session=session, page_url="/home", timestamp=timezone.now()
    )
    Event.objects.create(
        website=website, session=session, event_name="click", timestamp=timezone.now()
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("analytics-overview")
    response = client.get(url, {"website_id": website.id})
    assert response.status_code == 200
    assert "total_pageviews" in response.data
    assert "total_visitors" in response.data
    assert "total_sessions" in response.data
    assert "total_events" in response.data
    assert "avg_session_duration" in response.data
    assert "bounce_rate" in response.data


@pytest.mark.django_db
def test_analytics_timeseries_authenticated(client, django_user_model):
    org = Organization.objects.create(name="TestOrg")
    user = django_user_model.objects.create_user(
        username="user2", email="user2@test.com", password="pass", organization=org
    )
    website = Website.objects.create(
        name="TestSite2", domain="test2.com", organization=org
    )
    session = Session.objects.create(
        website=website, session_id="sess2", started_at=timezone.now()
    )
    PageView.objects.create(
        website=website, session=session, page_url="/about", timestamp=timezone.now()
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("analytics-timeseries")
    response = client.get(url, {"website_id": website.id})
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert "date" in response.data[0]
    assert "pageviews" in response.data[0]
    assert "visitors" in response.data[0]
    assert "sessions" in response.data[0]




from ..utils.cache_utils import AnalyticsCache  
from django.core.cache import cache

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
    key = f"v1:analytics_overview:{org_id}:{website_id}:{days}"
    AnalyticsCache.invalidate_organization_cache(org_id)
    assert AnalyticsCache.get_overview_stats(org_id, website_id, days) is None