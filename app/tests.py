# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Profile
import json

class AuthServiceTests(APITestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123',
            # ~ password2='testpass123'
        )
        self.client = APIClient()
    
    def test_user_registration(self):
        """Test user can register successfully"""
        url = reverse('user-create')
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login_success(self):
        """Test user can login and get tokens"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_login_invalid_credentials(self):
        """Test login fails with wrong credentials"""
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_get_user_profile_authenticated(self):
        """Test authenticated user can retrieve their profile"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('profile-me')
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_user_profile_unauthenticated(self):
        """Test unauthenticated user cannot access profile"""
        url = reverse('profile-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile(self):
        """Test user can update their profile"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('profile-me')
        data = {
            'bio': 'Updated bio',
            'location': 'Test City'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')
        
        # Verify the update in database
        profile = Profile.objects.get(user=self.regular_user)
        self.assertEqual(profile.bio, 'Updated bio')

    def test_get_current_user_info(self):
        """Test user can retrieve their own information"""
        user = self.regular_user
        self.client.force_authenticate(user=user)
        url = reverse('user-me')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_delete_user_account(self):
        """Test user can delete their own account"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-delete')
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_list_users_admin_only(self):
        """Test only admin can list all users"""
        # Try as regular user - should be denied
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try as admin - should be allowed
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_admin_only(self):
        """Test only admin can create users via admin endpoint"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-list')
        data = {
            'username': 'admincreated',
            'password': 'testpass123',
            'password2':'testpass123'
				}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should be able to create
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_jwt_token_contains_custom_claims(self):
        """Test JWT tokens contain custom claims"""
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'adminpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token contains custom claims
        self.assertEqual(response.data['is_admin'], True)
        self.assertEqual(response.data['username'], 'admin')

    def test_profile_auto_creation(self):
        """Test profile is automatically created for new users"""
        # Create a new user via registration
        url = reverse('user-create')
        data = {
            'username': 'autoprofile',
            'email': 'auto@test.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify profile was created
        user = User.objects.get(username='autoprofile')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        url = reverse('user-create')
        data = {
            'username': 'mismatchuser',
            'email': 'mismatch@test.com',
            'password': 'password123',
            'password2': 'differentpassword'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_duplicate_username(self):
        """Test registration fails with duplicate username"""
        url = reverse('user-create')
        data = {
            'username': 'testuser',  # Already exists
            'email': 'new@test.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class ProfileModelTests(TestCase):
    def test_profile_creation_signal(self):
        """Test profile is automatically created when user is created"""
        user = User.objects.create_user(
            username='signaluser',
            password='testpass123'
        )
        
        # Profile should be created automatically via signal
        self.assertTrue(Profile.objects.filter(user=user).exists())
        
    def test_profile_str_representation(self):
        """Test profile string representation"""
        user = User.objects.create_user(username='strtest', password='test123')
        profile = Profile.objects.get(user=user)
        
        self.assertEqual(str(profile), "strtest's profile")

class PermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='permadmin', password='admin123'
        )
        self.user = User.objects.create_user(
            username='permuser', password='user123'
        )
        self.client = APIClient()

    def test_is_admin_user_permission(self):
        """Test IsAdminUser permission works correctly"""
        url = reverse('user-list')
        
        # Regular user should be denied
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin user should be allowed
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_authenticated_or_read_only(self):
        """Test IsAuthenticatedOrReadOnly permission"""
        # Unauthenticated user should be able to read user detail (if implemented)
        # This depends on your specific implementation
        
    def test_allow_any_permission(self):
        """Test AllowAny permission for registration and login"""
        registration_url = reverse('user-create')
        login_url = reverse('login')
        
        # Both endpoints should be accessible without authentication
        response = self.client.get(registration_url)  # If GET is allowed
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED])
        
        response = self.client.post(login_url, {})
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])
