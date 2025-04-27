"""
Test the Organizations API endpoints.
"""

from core.models import Organization
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from organizations.serializers import (
    OrganizationSerializer,
    OrganizationDetailSerializer
)

# from organizations import urls

ORGANIZATION_URL = reverse('organizations:organization-list')


def create_organization(user, **params):
    """Create and return a sample organization."""
    defaults = {
        'name': 'Test Organization',
        'description': 'Test description',
        'email': 'org@example.com',
        'is_parent': True,
        'is_active': True,
    }
    defaults.update(params)

    return Organization.objects.create(owner=user, **defaults)


def get_organization_detail_url(organization_id):
    """Return the URL for the organization detail view."""
    return reverse('organizations:organization-detail', args=[organization_id])


def create_user(**params):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(**params)


class PublicOrganizationsAPITests(TestCase):
    """Test the publicly available organizations API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_organizations_unauthorized(self):
        """Test that listing organizations is unauthorized."""
        # print(urls.router.urls)
        response = self.client.get(ORGANIZATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_unauthorized(self):
        """Test that creating an organization is unauthorized."""
        payload = {
            'name': 'Test Organization',
            'description': 'Test description',
            'email': 'org@example.com',
            'is_parent': True,
            'is_active': True,
        }
        response = self.client.post(ORGANIZATION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrganizationsAPITests(TestCase):
    """Test the authorized user organizations API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_create_organization_successful(self):
        """Test creating a new organization is successful."""
        payload = {
            'name': 'Test Organization',
            'description': 'Test description',
            'email': 'org@example.com',
            'is_parent': True,
            'is_active': True,
        }
        response = self.client.post(ORGANIZATION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_organizations(self):
        """Test retrieving a list of organizations."""
        create_organization(user=self.user, email='org1@example.com')
        create_organization(user=self.user, name='Another Organization', email='org@example.com')
        response = self.client.get(ORGANIZATION_URL)
        organizations = Organization.objects.all().order_by('-id')
        serializer = OrganizationSerializer(organizations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for org_response, org_serialized in zip(response.data, serializer.data):
            self.assertEqual(org_response['id'], org_serialized['id'])
            self.assertEqual(org_response['name'], org_serialized['name'])
            self.assertEqual(org_response['email'], org_serialized['email'])

    def test_organizations_by_user(self):
        """Test retrieving organizations by user."""
        create_organization(user=self.user, email='org3@example.com')
        other_user = create_user(
            email='other@example.com',
            password='testpass123',
        )
        create_organization(
            user=other_user,
            name='Other User Organization',
            email='org4@example.com',
        )
        response = self.client.get(ORGANIZATION_URL)
        organizations = Organization.objects.filter(owner=self.user).order_by('-id')
        serializer = OrganizationSerializer(organizations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for org_response, org_serialized in zip(response.data, serializer.data):
            self.assertEqual(org_response['id'], org_serialized['id'])
            self.assertEqual(org_response['name'], org_serialized['name'])
            self.assertEqual(org_response['email'], org_serialized['email'])

    def test_retrieve_organization_by_id(self):
        """Test retrieving an organization by ID."""
        organization = create_organization(user=self.user)
        url = get_organization_detail_url(organization.id)
        response = self.client.get(url)
        serializer = OrganizationDetailSerializer(organization)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], serializer.data['id'])
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['email'], serializer.data['email'])
        self.assertIsNotNone(serializer.data['is_parent'])
        self.assertIsNotNone(serializer.data['is_active'])

    def test_create_organization(self):
        """Test creating an organization."""
        payload = {
            'name': 'Test Organization',
            'description': 'Test description',
            'email': 'org@example.com',
        }
        response = self.client.post(ORGANIZATION_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.get(id=response.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(organization, k), v)
        self.assertEqual(organization.owner, self.user)

    def test_partial_update_organization(self):
        """Test partially updating an organization."""
        organization = create_organization(user=self.user)
        payload = {
            'name': 'Updated Organization',
            'description': 'Updated description',
        }
        url = get_organization_detail_url(organization.id)
        response = self.client.patch(url, payload)
        organization.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(organization.name, payload['name'])
        self.assertEqual(organization.description, payload['description'])

    def test_full_update_organization(self):
        """Test fully updating an organization."""
        organization = create_organization(user=self.user)
        payload = {
            'name': 'Updated Organization',
            'description': 'Updated description',
            'email': 'test@example.com',
            'is_parent': False,
            'is_active': False,
        }
        url = get_organization_detail_url(organization.id)
        response = self.client.put(url, payload)
        organization.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(organization.name, payload['name'])
        self.assertEqual(organization.description, payload['description'])

    def test_delete_organization(self):
        """Test deleting an organization."""
        organization = create_organization(user=self.user)
        url = get_organization_detail_url(organization.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        organizations = Organization.objects.filter(id=organization.id)
        self.assertFalse(organizations.exists())

    def test_organization_not_found(self):
        """Test organization not found."""
        url = get_organization_detail_url(99999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
