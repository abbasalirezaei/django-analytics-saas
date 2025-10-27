from rest_framework import permissions

class OrganizationPermission(permissions.BasePermission):
    """
    Grouped permissions for organization-related access.
    """

    def has_permission(self, request, view):
        if not request.organization:
            return False

        if hasattr(view, 'permission_type'):
            if view.permission_type == 'admin':
                return self.is_admin(request)
            elif view.permission_type == 'active':
                return self.is_active(request)

        return True

    def is_admin(self, request):
        return hasattr(request.user, 'organization') and request.user.role == 'admin'

    def is_active(self, request):
        return request.organization.is_active


# --- Add missing permission classes for API compatibility ---
class HasOrganizationAccess(permissions.BasePermission):
    """
    Allows access only to users with an active organization.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'organization') and request.user.organization and request.user.organization.is_active

class IsOrganizationAdmin(permissions.BasePermission):
    """
    Allows access only to admin users of the organization.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'admin' and hasattr(request.user, 'organization') and request.user.organization and request.user.organization.is_active