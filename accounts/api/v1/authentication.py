from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.services.auth_services import validate_api_key


class OrganizationAuthUser:
    def __init__(self, organization):
        if organization is None:
            raise ValueError("Organization cannot be None")
        self.organization = organization
        self.pk = organization.pk
        self.id = organization.id

    @property
    def is_authenticated(self):
        return True


class APIKeyAuthentication(BaseAuthentication):
    """
    Authenticate requests using API Key in headers.
    Header: X-API-Key: your_api_key_here
    """

    def authenticate(self, request):
        api_key = self.get_api_key(request)

        if not api_key:
            return None

        organization = validate_api_key(api_key)

        if organization is None:
            raise AuthenticationFailed("Invalid or missing API key")

        user = OrganizationAuthUser(organization)
        return (user, organization)

    def get_api_key(self, request):
        # Check header first
        api_key = request.headers.get("X-API-Key")

        # Fallback to query parameter (for GET requests)
        if not api_key:
            api_key = request.GET.get("api_key")

        return api_key

    def authenticate_header(self, request):
        return "APIKey"
