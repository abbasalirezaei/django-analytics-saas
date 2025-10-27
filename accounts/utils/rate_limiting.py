from rest_framework.throttling import SimpleRateThrottle

class OrganizationRateThrottle(SimpleRateThrottle):
    """
    Rate limiting per organization
    """
    rate = '1000/hour'  # Configurable rate
    
    def get_cache_key(self, request, view):
        if not request.organization:
            return None
        return f"throttle_org_{request.organization.id}"

class UserRateThrottle(SimpleRateThrottle):
    """
    Rate limiting per user
    """
    rate = '100/hour'  # Configurable rate
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        return f"throttle_user_{request.user.id}"