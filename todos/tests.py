from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user_success(self):
        """Test creating a new user with valid credentials"""
        email = "test@example.com"
        name = "Test User"
        password = "testpass123"
        
        user = self.User.objects.create_user(
            email=email,
            name=name,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_email_normalized(self):
        """Test email is normalized when creating user"""
        email = "test@EXAMPLE.com"
        user = self.User.objects.create_user(
            email=email,
            name="Test User",
            password="test123"
        )
        
        self.assertEqual(user.email, email.lower())

    def test_create_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email=None,
                name="Test User",
                password="test123"
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email="",
                name="Test User",
                password="test123"
            )

    def test_create_user_without_password(self):
        """Test creating user without password"""
        email = "test@example.com"
        user = self.User.objects.create_user(
            email=email,
            name="Test User",
            password=None
        )
        
        self.assertEqual(user.email, email)
        self.assertFalse(user.has_usable_password())

    @patch('todos.models.BaseUserManager.normalize_email')
    def test_normalize_email_called(self, mock_normalize):
        """Test that normalize_email method is called"""
        mock_normalize.return_value = "test@example.com"
        
        self.User.objects.create_user(
            email="TEST@EXAMPLE.COM",
            name="Test User",
            password="test123"
        )
        
        mock_normalize.assert_called_once_with("TEST@EXAMPLE.COM")

    def test_create_user_minimum_fields(self):
        """Test creating user with minimum required fields"""
        user = self.User.objects.create_user(
            email="test@example.com",
            name="Test User"
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")

    def test_create_user_save_called(self):
        """Test that save method is called when creating user"""
        with patch.object(self.User, 'save') as mock_save:
            self.User.objects.create_user(
                email="test@example.com",
                name="Test User",
                password="test123"
            )
            
            mock_save.assert_called_once()
