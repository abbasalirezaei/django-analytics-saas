from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	# Keep admin minimal until migrations are applied
	list_display = ['name', 'api_key', 'is_active']
	search_fields = ['name']


@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
	# Avoid referencing new fields until migrations are in sync
	list_display = ['username', 'email', 'is_active']
