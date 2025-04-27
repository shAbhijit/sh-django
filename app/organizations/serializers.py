"""
Serializer for the Organization model.
"""
from rest_framework import serializers
from core.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Organization model.
    """
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'email',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class OrganizationDetailSerializer(OrganizationSerializer):
    """
    Serializer for the Organization model with additional fields.
    """
    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + (
            'is_parent',
            'is_active',
        )
