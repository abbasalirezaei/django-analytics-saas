"""
Service layer for user-related operations
"""
from typing import Optional, Dict, Any
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework.exceptions import ValidationError

from accounts.models import Organization
from accounts.utils.common import validate_input, get_cached_data, set_cached_data

User = get_user_model()

class UserService:
    """
    Service class for user-related operations
    """
    
    @staticmethod
    def create_user(data: Dict[str, Any], organization: Organization) -> User:
        """
        Create a new user in an organization
        """
        required_fields = ['username', 'email', 'password', 'role']
        is_valid, errors = validate_input(data, required_fields)
        
        if not is_valid:
            raise ValidationError(errors)
            
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            organization=organization,
            role=data['role']
        )
        
        return user
    
    @staticmethod
    def get_user_with_organization(user_id: int) -> Optional[User]:
        """
        Get user with organization details
        Uses select_related for efficient querying
        """
        return User.objects.select_related(
            'organization'
        ).get(id=user_id)
    
    @staticmethod
    def get_organization_users(organization_id: int, role: Optional[str] = None):
        """
        Get all users in an organization with optional role filter
        """
        users = User.objects.filter(organization_id=organization_id)
        if role:
            users = users.filter(role=role)
            
        return users.select_related('organization')