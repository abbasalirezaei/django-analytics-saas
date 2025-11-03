from .models import Organization

class OrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.organization = None

        if hasattr(request, "user") and request.user.is_authenticated:
            org = getattr(request.user, "organization", None)
            if org and org.is_active:
                request.organization = org

        elif hasattr(request, "auth") and isinstance(request.auth, Organization):
            if request.auth.is_active:
                request.organization = request.auth

        response = self.get_response(request)

        return response