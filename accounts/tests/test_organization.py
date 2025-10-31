import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Organization
from accounts.services.organization_service import OrganizationService

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def org_data():
    return {
        "organization_name": "Test Org",
        "admin_username": "admin",
        "admin_email": "admin@test.com",
        "admin_password": "securepass123",
    }


@pytest.mark.django_db
class TestOrganization:
    def test_create_organization(self, api_client, org_data):
        """Test organization creation"""
        url = reverse("register")
        response = api_client.post(url, org_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "api_key" in response.data

        # Verify organization in database
        org = Organization.objects.get(name=org_data["organization_name"])
        assert org.is_active == True

        # Verify admin user was created
        user = User.objects.get(username=org_data["admin_username"])
        assert user.organization == org
        assert user.role == "admin"

    def test_organization_api_key_auth(self, api_client, org_data):
        """Test API key authentication"""
        org, _ = OrganizationService.create_organization(org_data)

        # Test with valid API key
        api_client.credentials(HTTP_X_API_KEY=org.api_key)
        url = reverse("organization-profile")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test with invalid API key
        api_client.credentials(HTTP_X_API_KEY="invalid-key")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_organization_user_management(self, api_client, org_data):
        """Test user management in organization"""
        org, admin = OrganizationService.create_organization(org_data)
        api_client.force_authenticate(user=admin)

        # Test user creation
        user_data = {
            "username": "testuser",
            "email": "user@test.com",
            "password": "userpass123",
            "role": "user",
        }
        url = reverse("user-list-create")
        response = api_client.post(url, user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Verify user was created with correct organization
        user = User.objects.get(username=user_data["username"])
        assert user.organization == org
        assert user.role == "user"


@pytest.mark.django_db
class TestRateLimiting:
    def test_rate_limiting(self, api_client, org_data):
        """Test rate limiting"""
        org, _ = OrganizationService.create_organization(org_data)
        api_client.credentials(HTTP_X_API_KEY=org.api_key)
        url = reverse("organization-profile")

        # Make requests up to the limit
        for _ in range(5):
            response = api_client.get(url)
            assert response.status_code == status.HTTP_200_OK

        # This request should be rate limited
        response = api_client.get(url)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
