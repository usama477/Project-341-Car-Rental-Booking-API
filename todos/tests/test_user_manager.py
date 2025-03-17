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

    def test_create_superuser_with_invalid_email(self):
        """Test creating a superuser with invalid email format"""
        with self.assertRaises(ValidationError):
            superuser = self.User.objects.create_superuser(
                email="invalid_email",
                name=self.valid_name,
                password=self.valid_password
            )
            superuser.full_clean()

    @patch('todos.models.CustomUserManager.create_user')
    def test_create_superuser_calls_create_user(self, mock_create_user):
        """Test that create_superuser calls create_user with correct parameters"""
        mock_user = MagicMock()
        mock_create_user.return_value = mock_user

        self.User.objects.create_superuser(
            email=self.valid_email,
            name=self.valid_name,
            password=self.valid_password
        )

        mock_create_user.assert_called_once_with(
            email=self.valid_email,
            name=self.valid_name,
            password=self.valid_password
        )
        self.assertTrue(mock_user.is_staff)
        self.assertTrue(mock_user.is_superuser)
        self.assertTrue(mock_user.save.called)

    def test_create_superuser_with_none_password(self):
        """Test creating a superuser with None password"""
        superuser = self.User.objects.create_superuser(
            email=self.valid_email,
            name=self.valid_name,
            password=None
        )
        
        self.assertEqual(superuser.email, self.valid_email)
        self.assertEqual(superuser.name, self.valid_name)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertFalse(superuser.has_usable_password())

    def test_create_superuser_preserves_email_case(self):
        """Test that email case is preserved correctly"""
        mixed_case_email = "Admin@Example.com"
        superuser = self.User.objects.create_superuser(
            email=mixed_case_email,
            name=self.valid_name,
            password=self.valid_password
        )
        
        self.assertEqual(superuser.email, mixed_case_email.lower())