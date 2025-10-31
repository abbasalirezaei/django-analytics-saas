"""
Service layer for organization-related operations
"""
from typing import Any, Dict, Optional, Tuple

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from accounts.models import Organization
from accounts.utils.common import get_cached_data, set_cached_data, validate_input

User = get_user_model()


class OrganizationService:
    """
    Service class for organization-related operations
    """

    @staticmethod
    def create_organization(data: Dict[str, Any]) -> Tuple[Organization, User]:
        """
        Create a new organization and admin user
        """
        required_fields = [
            "organization_name",
            "admin_username",
            "admin_email",
            "admin_password",
        ]
        is_valid, errors = validate_input(data, required_fields)

        if not is_valid:
            raise ValidationError(errors)

        with transaction.atomic():
            # Create organization
            organization = Organization.objects.create(name=data["organization_name"])

            # Create admin user
            user = User.objects.create_user(
                username=data["admin_username"],
                email=data["admin_email"],
                password=data["admin_password"],
                first_name=data.get("admin_first_name", ""),
                last_name=data.get("admin_last_name", ""),
                organization=organization,
                role="admin",
            )

        return organization, user

    @staticmethod
    def regenerate_api_key(organization_id: int) -> str:
        """
        Regenerate API key for an organization
        """
        organization = Organization.objects.get(id=organization_id)
        organization.regenerate_api_key()
        return organization.api_key

    @staticmethod
    def get_organization_by_api_key(api_key: str) -> Optional[Organization]:
        """
        Get organization by API key with caching
        """
        # Try cache first
        cached_org = get_cached_data(f"org_api_key:{api_key}")
        if cached_org:
            return cached_org

        try:
            organization = Organization.objects.select_related("users").get(
                api_key=api_key, is_active=True
            )

            # Cache for future requests
            set_cached_data(f"org_api_key:{api_key}", organization)
            return organization
        except Organization.DoesNotExist:
            return None
