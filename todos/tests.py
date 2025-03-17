from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock

class TestCustomUserManager(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.valid_email = "admin@example.com"
        self.valid_name = "Admin User"
        self.valid_password = "adminpass123"

    def test_create_superuser_success(self):
        """Test creating a superuser with valid credentials"""
        superuser = self.User.objects.create_superuser(
            email=self.valid_email,
            name=self.valid_name,
            password=self.valid_password
        )
        
        self.assertEqual(superuser.email, self.valid_email)
        self.assertEqual(superuser.name, self.valid_name)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(self.valid_password))

    def test_create_superuser_without_email(self):
        """Test creating a superuser without email should raise error"""
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="",
                name=self.valid_name,
                password=self.valid_password
            )

    def test_create_user_success(self):
        """Test creating a new user with valid credentials"""
        user = self.User.objects.create_user(
            email=self.valid_email,
            name=self.valid_name,
            password=self.valid_password
        )
        
        self.assertEqual(user.email, self.valid_email)
        self.assertEqual(user.name, self.valid_name)
        self.assertTrue(user.check_password(self.valid_password))
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
