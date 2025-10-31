import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import Organization, User
from accounts.services.auth_services import validate_api_key


@pytest.mark.django_db
def test_validate_api_key():
    organization = Organization.objects.create(
        name="Test Org", api_key="testkey123", is_active=True
    )
    result = validate_api_key("testkey123")
    assert result == organization


@pytest.mark.django_db
def test_register_organization():
    client = APIClient()
    url = reverse("register")
    data = {
        "organization_name": "New Org",
        "admin_username": "adminuser",
        "admin_email": "admin@example.com",
        "admin_password": "securepassword123",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Organization.objects.filter(name="New Org").exists()
