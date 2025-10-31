from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from accounts.models import Organization


def validate_api_key(api_key):
    """
    Validate the API key and return the associated organization.
    Uses caching to improve performance.
    """
    if not api_key:
        return None

    # Check cache first
    cached_organization = cache.get(f"organization_{api_key}")
    if cached_organization:
        return cached_organization

    try:
        organization = Organization.objects.get(api_key=api_key, is_active=True)
        # Cache the organization for future requests
        cache.set(
            f"organization_{api_key}", organization, timeout=3600
        )  # Cache for 1 hour
        return organization
    except ObjectDoesNotExist:
        raise ValueError("Invalid or inactive API key")
    except MultipleObjectsReturned:
        raise ValueError("Multiple organizations with the same API key")
