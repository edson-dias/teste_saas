from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User, Company


class UserViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        company = Company(
            corporate_name='test_company',
            trade_name='test_trade_name',
            cnpj='12345678901234'
        )
        company.save()
        user = User.objects.create_user(
            first_name='test',
            last_name='user',
            email='test-user@hotmail.com',
            password='123456789'
        )
        company.user.add(user)
        cls.company = company
        cls.members_url = reverse('user-members')
        cls.create_url = reverse('user-list')

    def test_user_list_returns_200(self):
        data = {'company_id': self.company.id}
        response = self.client.get(self.members_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_list_returns_400(self):
        data = {}
        response = self.client.get(self.members_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_create_returns_201(self):
        data = {
            'first_name': 'user',
            'last_name': 'test',
            'email': 'user-test@gmail.com',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_create_returns_400_when_password_is_empty(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'edson_dias@hotmail.com',
            'password': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_create_returns_400_when_email_is_empty(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': '',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_create_returns_400_when_email_is_invalid(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'email123',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_create_returns_400_when_email_is_already_registered(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test-user@hotmail.com',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_create_creates_a_new_user(self):
        data = {
            'first_name': 'django',
            'last_name': 'test',
            'email': 'django@gmail.com',
            'password': '123456'
        }
        count_before_post = User.objects.all().count()
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(count_before_post, User.objects.count() - 1)
    
