from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.permissions import HasOrganizationAccess, IsOrganizationAdmin
from accounts.api.v1.serializers import (
    CustomTokenObtainPairSerializer,
    OrganizationSerializer,
    RegisterSerializer,
    UserSerializer,
    WebsiteSerializer,
)
from accounts.models import Organization
from tracking.models.website import Website

User = get_user_model()

# ============================================================================
# AUTHENTICATION
# ============================================================================


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterOrganizationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = serializer.save()
        organization = (
            Organization.objects.filter(id=organization.id)
            .prefetch_related("users")
            .first()
        )
        return Response(
            {
                "message": "Organization and admin user created successfully",
                "organization": OrganizationSerializer(organization).data,
                "api_key": organization.api_key,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================================
# PROFILE
# ============================================================================


class OrganizationProfileView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, HasOrganizationAccess]

    def get_object(self):
        return Organization.objects.prefetch_related(
            Prefetch("users", queryset=User.objects.only("id", "username"))[:50]
        ).get(id=self.request.user.organization.id)


class RegenerateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def post(self, request):
        organization = request.user.organization
        organization.api_key = None
        organization.save()
        organization.refresh_from_db()
        return Response(
            {
                "message": "API key regenerated successfully",
                "new_api_key": organization.api_key,
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ============================================================================
# USER MANAGEMENT
# ============================================================================


class UserListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(organization=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.filter(organization=self.request.user.organization)


# ============================================================================
# WEBSITE MANAGEMENT
# ============================================================================


class WebsiteListCreateAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasOrganizationAccess]
    serializer_class = WebsiteSerializer

    def get_queryset(self):
        return Website.objects.filter(
            organization=self.request.user.organization
        ).select_related("organization")

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class WebsiteDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, HasOrganizationAccess]
    serializer_class = WebsiteSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Website.objects.filter(organization=self.request.user.organization)
