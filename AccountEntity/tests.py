from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer


class AccountEntityManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            account_name="Test User",
            password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.account_name, "Test User")
        # Add more assertions as needed

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin",
            account_name="admin",
            email="admin@example.com",
            password="adminpassword"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.account_name, "admin")
        # Add more assertions as needed


User = get_user_model()


class RegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'account_name': 'John Doe',
            'username': 'A12345',
            'sdt': '123456789',
            'password': 'Password123',
            're_password': 'Password123',
        }
        self.invalid_data = {
            'account_name': '',
            'username': 'A1',
            'sdt': '123',
            'password': 'password',
            're_password': 'pass',
        }

    def test_valid_serializer_data(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        serializer = RegisterSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('account_name', serializer.errors)
        self.assertIn('username', serializer.errors)
        self.assertIn('sdt', serializer.errors)
        self.assertIn('password', serializer.errors)
        self.assertIn('re_password', serializer.errors)

    def test_create_user(self):
        serializer = RegisterSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.valid_data['username'])
