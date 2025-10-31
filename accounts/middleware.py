from django.utils.deprecation import MiddlewareMixin

from .models import Organization


class OrganizationMiddleware(MiddlewareMixin):
    """
    Adds organization to request object for easy access in views
    """

    def process_request(self, request):
        # Initialize request.organization as None
        request.organization = None

        # If user is authenticated and has organization
        if hasattr(request, "user") and request.user.is_authenticated:
            org = getattr(request.user, "organization", None)
            if org and org.is_active:
                request.organization = org

        # If API key authentication was used
        elif hasattr(request, "auth") and isinstance(request.auth, Organization):
            if request.auth.is_active:
                request.organization = request.auth

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Additional processing before view is called
        """
        # You can add organization-specific logic here
        pass
