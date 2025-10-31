from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.v1 import views

urlpatterns = [
    # Authentication
    path(
        "auth/login/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", views.RegisterOrganizationView.as_view(), name="register"),
    # Profile
    path(
        "organization/profile/",
        views.OrganizationProfileView.as_view(),
        name="organization-profile",
    ),
    path(
        "organization/regenerate-api-key/",
        views.RegenerateAPIKeyView.as_view(),
        name="regenerate-api-key",
    ),
    path("user/profile/", views.UserProfileView.as_view(), name="user-profile"),
    # User Management
    path("users/", views.UserListCreateAPI.as_view(), name="user-list-create"),
    path("users/<int:id>/", views.UserDetailAPI.as_view(), name="user-detail"),
    # Website Management
    path("websites/", views.WebsiteListCreateAPI.as_view(), name="website-list-create"),
    path("websites/<int:id>/", views.WebsiteDetailAPI.as_view(), name="website-detail"),
]
