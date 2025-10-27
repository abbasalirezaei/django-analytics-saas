from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from accounts.models import Organization
from accounts.middleware import OrganizationMiddleware
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class OrganizationMiddlewareTest(TestCase):
    def setUp(self):
        self.middleware = OrganizationMiddleware(get_response=lambda request: None)
        self.request = HttpRequest()
        self.organization = Organization.objects.create(
            name="Test Org",
            is_active=True
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            organization=self.organization
        )
        
    def tearDown(self):
        cache.clear()
        
    def test_process_request_with_authenticated_user(self):
        """Test middleware with authenticated user"""
        self.request.user = self.user
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.organization, self.organization)
        
    def test_process_request_with_anonymous_user(self):
        """Test middleware with anonymous user"""
        self.request.user = AnonymousUser()
        self.middleware.process_request(self.request)
        self.assertIsNone(self.request.organization)
        
    def test_process_request_with_inactive_organization(self):
        """Test middleware with inactive organization"""
        self.organization.is_active = False
        self.organization.save()
        self.request.user = self.user
        self.middleware.process_request(self.request)
        self.assertIsNone(self.request.organization)
        
    def test_process_request_with_api_key(self):
        """Test middleware with API key authentication"""
        self.request.user = AnonymousUser()
        self.request.auth = self.organization
        self.middleware.process_request(self.request)
        self.assertEqual(self.request.organization, self.organization)