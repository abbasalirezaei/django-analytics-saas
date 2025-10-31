import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.services.auth_services import validate_api_key
from accounts.services.organization_service import OrganizationService
from accounts.services.user_service import UserService

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "user",
    }


@pytest.mark.django_db
class TestAuthServices:
    def test_validate_api_key(self, org_data):
        """Test API key validation"""
        org, _ = OrganizationService.create_organization(org_data)

        # Test valid API key
        result = validate_api_key(org.api_key)
        assert result == org

        # Test invalid API key
        result = validate_api_key("invalid-key")
        assert result is None

        # Test inactive organization
        org.is_active = False
        org.save()
        result = validate_api_key(org.api_key)
        assert result is None


@pytest.mark.django_db
class TestUserService:
    def test_create_user(self, user_data, org_data):
        """Test user creation"""
        org, _ = OrganizationService.create_organization(org_data)

        # Test creating a regular user
        user = UserService.create_user(user_data, org)
        assert user.username == user_data["username"]
        assert user.organization == org
        assert user.role == "user"

        # Test creating a duplicate user
        with pytest.raises(Exception):
            UserService.create_user(user_data, org)

    def test_get_organization_users(self, user_data, org_data):
        """Test retrieving organization users"""
        org, admin = OrganizationService.create_organization(org_data)
        user = UserService.create_user(user_data, org)

        # Test getting all users
        users = UserService.get_organization_users(org.id)
        assert users.count() == 2  # admin + regular user

        # Test filtering by role
        admin_users = UserService.get_organization_users(org.id, role="admin")
        assert admin_users.count() == 1
        assert admin_users.first() == admin
