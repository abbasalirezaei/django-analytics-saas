from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "api_key", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    ordering = ["name"]
    readonly_fields = ["api_key", "created_at"]


@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["username", "email", "role", "is_active", "organization"]
    list_filter = ["role", "is_active", "organization"]
    search_fields = ["username", "email"]
    ordering = ["username"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Organization Details", {"fields": ("organization", "role")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "organization",
                    "role",
                ),
            },
        ),
    )
