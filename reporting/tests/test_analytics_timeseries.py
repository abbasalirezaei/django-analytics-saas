import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models.organization import Organization
from tracking.models import PageView, Session, Website

@pytest.mark.django_db
def test_analytics_timeseries_authenticated(django_user_model):
    org = Organization.objects.create(name="TestOrg")
    user = django_user_model.objects.create_user(
        username="user2", email="user2@test.com", password="pass", organization=org
    )
    website = Website.objects.create(name="TestSite2", domain="test2.com", organization=org)
    session = Session.objects.create(website=website, session_id="sess2", started_at=timezone.now())
    PageView.objects.create(website=website, session=session, page_url="/about", timestamp=timezone.now())

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("analytics-timeseries")
    response = client.get(url, {"website_id": website.id})

    assert response.status_code == 200
    assert isinstance(response.data, list)
    for field in ["date", "pageviews", "visitors", "sessions"]:
        assert field in response.data[0]