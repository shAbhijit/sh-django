"""
Serializers for User API view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ManageUserSerializer(serializers.ModelSerializer):
    """Serializer for managing the authenticated user."""
    class Meta:
        model = get_user_model()
        fields = ['name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate user')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
