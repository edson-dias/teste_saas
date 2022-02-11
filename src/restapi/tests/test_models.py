import email
from typing import Type
from django.db import IntegrityError
from django.test import TestCase
from ..models import User, BaseUser

class UserModelTest(TestCase):
    def setUp(self):
        self.user = BaseUser(
            first_name='new',
            last_name='user',
            email='new_user@outlook.com',
            password='123456'
        )

    @classmethod
    def setUpTestData(cls):
        user = BaseUser(
            first_name='django',
            last_name='framework',
            email='django_framework@outlook.com',
            password='123456'
        )
        User.objects.create_user(user)

    def test_user_first_name_equals_django(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.first_name, 'django')
    
    def test_user_last_name_equals_framework(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.last_name, 'framework')
    
    def test_user_email_equals_django_framework(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.email, 'django_framework@outlook.com')

    def test_is_user_valid_fails_if_first_name_is_none(self):
        self.user.first_name = None
        with self.assertRaises(TypeError):
            User.objects.create_user(self.user)               
            
    def test_is_user_valid_fails_if_last_name_is_none(self):
        self.user.last_name = None
        with self.assertRaises(TypeError):
            User.objects.create_superuser(self.user)
    
    def test_is_user_valid_fails_if_email_is_none(self):
        self.user.email = None
        with self.assertRaises(TypeError):
            User.objects.create_superuser(self.user)
    
    def test_is_user_valid_fails_if_password_is_none(self):
        self.user.password = None
        with self.assertRaises(TypeError):
            User.objects.create_superuser(self.user)
    
    def test_create_user_fails_if_email_is_not_unique(self):
        self.user.email = 'django_framework@outlook.com'
        with self.assertRaises(IntegrityError):
            User.objects.create_user(self.user)
            
    def test_create_superuser_fails_if_email_is_not_unique(self):
        self.user.email = 'django_framework@outlook.com'
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(self.user)

