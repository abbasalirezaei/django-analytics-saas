import pytest
from django.urls import reverse
from rest_framework.test import APITestCase
from ..services.tracking_service import TrackingService

from tracking.models import Session
from tracking.tests.factories.factories import WebsiteFactory, SessionFactory
from tracking.api.v1.serializers import SessionStartSerializer
from rest_framework.test import APIClient

"""
test serviece
"""

@pytest.mark.django_db
def test_start_session_service_success():
    website = WebsiteFactory()
    domain = website.domain
    data = {
        "session_id": "abc123",
        "user_agent": "Mozilla/5.0 (iPhone)",
        "ip_address": "1.2.3.4",
        "country": "US",
        "browser": "Safari",
        "device_type": "mobile",
    }

    session, result = TrackingService.start_session(domain, data)

    assert session is not None
    assert result["status"] == "ok"
    assert Session.objects.filter(session_id="abc123").exists()

"""
test serializer with valid and invalid data
"""
@pytest.mark.django_db
def test_start_session_serializer_valid():
    website = WebsiteFactory()
    domain = website.domain
    data = {
        "session_id": "abc123",
        "user_agent": "Mozilla/5.0 (iPhone)",
        "ip_address": "1.2.3.4",
        "country": "US",
        "browser": "Safari",
        "device_type": "mobile",
        "domain": domain
    }
    serializer = SessionStartSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_start_session_serializer_invalid():
    # website = WebsiteFactory()
    # domain = website.domain
    data = {
        "session_id": "abc123",
        "user_agent": "Mozilla/5.0 (iPhone)",
        "ip_address": "1.2.3.4",
        "country": "US",
        "browser": "Safari",
        "device_type": "mobile",
        "domain": "nonexistent.com"
    }
    serializer = SessionStartSerializer(data=data)
    is_valid = serializer.is_valid()

    assert not is_valid
    assert "domain" in serializer.errors
    assert serializer.errors["domain"][0] == "Website with this domain does not exist or is inactive."


"""
test the view with valid and invalid data
"""
@pytest.mark.django_db
def test_start_session_success():
    client = APIClient()
    website = WebsiteFactory()
    domain = website.domain
    url = reverse("tracking:api-v1:session-start")
    
    data = SessionFactory.build()

    payload = {
        "domain": domain,
        "session_id": data.session_id,
        "user_agent": data.user_agent,
        "ip_address": data.ip_address,
        "country": data.country,
        "browser": data.browser,
        "device_type": data.device_type,
    }

    response = client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert response.data["status"] == "ok"

