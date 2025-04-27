"""
Test for user API endpoints.
"""

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        rest = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exist."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        rest = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            rest.data['email'],
            ['user with this email already exists.']
        )

    def test_password_too_short_error(self):
        """Test error returned if password less than 5 characters."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        rest = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for the user."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        rest = self.client.post(TOKEN_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_200_OK)
        self.assertIn('token', rest.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )

        payload = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'name': 'Test Name',
        }
        rest = self.client.post(TOKEN_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', rest.data)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        rest = self.client.post(TOKEN_URL, payload)
        self.assertEqual(rest.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', rest.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users."""
        rest = self.client.get(ME_URL)
        self.assertEqual(rest.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieve the profile logged in user"""
        rest = self.client.get(ME_URL)
        self.assertEqual(rest.status_code, status.HTTP_200_OK)
        self.assertEqual(rest.data, {
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        rest = self.client.post(ME_URL, {})
        self.assertEqual(rest.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'New Name',
            'password': 'newpassword123',
        }
        rest = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(rest.status_code, status.HTTP_200_OK)
