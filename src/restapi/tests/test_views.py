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
        cls.user = User.objects.create_user(
            first_name='test',
            last_name='user',
            email='test-user@hotmail.com',
            password='123456789'
        )
        company.user.add(cls.user)
        cls.company = company
        cls.members_url = reverse('user-company-user')
        cls.create_url = reverse('user-new')

    def test_company_user_returns_200_with_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {'company_id': self.company.id}
        response = self.client.get(self.members_url, data, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_company_user_returns_400_if_company_id_is_none(self):
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.get(self.members_url, data, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_company_user_returns_401_it_user_not_authenticated(self):
        data = {'company_id': self.company.id}
        response = self.client.get(self.members_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_user_without_authentication_returns_201(self):
        data = {
            'first_name': 'user',
            'last_name': 'test',
            'email': 'user-test@gmail.com',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_creates_user_returns_400_when_password_is_empty(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'edson_dias@hotmail.com',
            'password': ''
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_creates_user_returns_400_when_email_is_empty(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': '',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_creates_user_returns_400_when_email_is_invalid(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'email123',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_creates_user_returns_400_when_email_is_already_registered(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test-user@hotmail.com',
            'password': '123456'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_new_user_view_creates_a_new_user(self):
        data = {
            'first_name': 'django',
            'last_name': 'test',
            'email': 'django@gmail.com',
            'password': '123456'
        }
        count_before_post = User.objects.all().count()
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(count_before_post, User.objects.count() - 1)
    

class CompanyViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse('company-list')
        cls.create_url = reverse('company-new')

        cls.django_user = User.objects.create_user(
            first_name='django',
            last_name='user',
            email='admin@hotmail.com',
            password='admin123'
        )
        cls.another_user = User.objects.create_user(
            first_name='another',
            last_name='user',
            email='user@hotmail.com',
            password='123456'
        )
        company_django = Company(
            corporate_name='django_company',
            trade_name='django_trade_name',
            cnpj='12345678901234'
        )
        company_another = Company(
            corporate_name='another_company',
            trade_name='another_trade_name',
            cnpj='11111111111111'
        )
        company_django.save()
        company_another.save()
        company_django.user.add(cls.django_user)
        company_another.user.add(cls.another_user)

    def setUp(self):
        self.client.force_authenticate(user=self.django_user)
    
    def tearDown(self):
        self.client.force_authenticate(user=None)

    def test_list_companies_with_authentication_returns_200(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_companies_returns_only_one_company(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data), 1)
    
    def test_list_companies_returns_only_logged_user_companies(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['corporate_name'], 'django_company')

    def test_list_companies_returns_401_when_user_is_not_logged(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_creates_company_returns_201_without_authentication(self):
        self.client.force_authenticate(user=None)
        data = {
            'corporate_name': 'create',
            'trade_name': 'company',
            'cnpj': '99315678901234',
            'user': [self.another_user.id]
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_new_company_view_creates_a_new_company(self):
        self.client.force_authenticate(user=None)
        data = {
            'corporate_name': 'new',
            'trade_name': 'company',
            'cnpj': '11315678101234',
            'user': [self.another_user.id]
        }
        count_before_post = Company.objects.all().count()
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(count_before_post, Company.objects.count() - 1)