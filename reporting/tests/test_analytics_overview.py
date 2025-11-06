import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models.organization import Organization
from tracking.models import Event, PageView, Session, Website

@pytest.mark.django_db
def test_analytics_overview_authenticated(django_user_model):
    org = Organization.objects.create(name="TestOrg")
    user = django_user_model.objects.create_user(
        username="user1", email="user@test.com", password="pass", organization=org
    )
    website = Website.objects.create(name="TestSite", domain="test.com", organization=org)
    session = Session.objects.create(website=website, session_id="sess1", started_at=timezone.now())
    PageView.objects.create(website=website, session=session, page_url="/home", timestamp=timezone.now())
    Event.objects.create(website=website, session=session, event_name="click", timestamp=timezone.now())

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("analytics-overview")
    response = client.get(url, {"website_id": website.id})

    assert response.status_code == 200
    for field in ["total_pageviews", "total_visitors", "total_sessions", "total_events", "avg_session_duration", "bounce_rate"]:
        assert field in response.data