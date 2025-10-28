from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Organization

from tracking.models.website import Website

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'api_key', 'created_at', 'is_active']
        read_only_fields = ['api_key', 'created_at']

    def to_representation(self, instance):
        """
        Optimize the serialized output by only including necessary fields.
        """
        representation = super().to_representation(instance)
        representation.pop('api_key', None)  # Remove sensitive data
        return representation


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'domain', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_domain(self, value):
        """
        Validate that the domain is unique for the organization
        """
        # This validation will be handled in the view
        return value


class UserSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'organization', 'role', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']


class RegisterSerializer(serializers.Serializer):
    organization_name = serializers.CharField(max_length=255)
    admin_username = serializers.CharField(max_length=150)
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(
        write_only=True, validators=[validate_password])
    admin_first_name = serializers.CharField(max_length=30, required=False)
    admin_last_name = serializers.CharField(max_length=30, required=False)

    def validate_admin_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_admin_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        # Create organization
        organization = Organization.objects.create(
            name=validated_data['organization_name']
        )

        # Create admin user
        user = User.objects.create_user(
            username=validated_data['admin_username'],
            email=validated_data['admin_email'],
            password=validated_data['admin_password'],
            first_name=validated_data.get('admin_first_name', ''),
            last_name=validated_data.get('admin_last_name', ''),
            organization=organization,
            role='admin'
        )

        return organization  


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        if user.organization:
            token['organization_id'] = user.organization.id
            token['organization_name'] = user.organization.name
        else:
            token['organization_id'] = None
            token['organization_name'] = None

        token['role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role,
            },
            'organization': {
                'id': self.user.organization.id,
                'name': self.user.organization.name,
            }
        })

        return data
