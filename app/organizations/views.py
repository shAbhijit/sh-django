"""
View for organizations API
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from core.models import Organization
from organizations import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Organization model.
    """
    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'post', 'patch', 'delete', 'put']

    def get_queryset(self):
        """
        Optionally restricts the returned organizations to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        return self.queryset.filter(owner=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Set the owner to the authenticated user."""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'list':
            return serializers.OrganizationDetailSerializer
        return self.serializer_class
