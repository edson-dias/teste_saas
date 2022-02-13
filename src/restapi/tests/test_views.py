from unittest.mock import Mock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User, Company
from ..views import get_company_data_from_external_api


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
        cls.create_url = reverse('user-list')
        cls.list_url = reverse('user-companies')

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
    
    def test_get_logged_user_companies_returns_200_with_authentication_(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_logged_user_companies_returns_only_one_company(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(len(response.data), 1)
    
    def test_get_logged_user_companies_returns_only_logged_user_companies(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, format='json')
        self.client.force_authenticate(user=None)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['corporate_name'], 'test_company')

    def test_get_logged_user_companies_returns_401_when_user_is_not_logged(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class CompanyViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
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
        cls.company_django = Company(
            corporate_name='django_company',
            trade_name='django_trade_name',
            cnpj='12345678901234'
        )
        cls.company_another = Company(
            corporate_name='another_company',
            trade_name='another_trade_name',
            cnpj='11111111111111'
        )
        cls.company_django.save()
        cls.company_another.save()
        cls.company_django.user.add(cls.django_user)
        cls.company_another.user.add(cls.another_user)

        cls.company_members_url = reverse('company-members', args=[cls.company_django.id])
        cls.registry_member_url = reverse('company-registry-member')
        cls.create_url = reverse('company-list')


    def setUp(self):
        self.client.force_authenticate(user=self.django_user)
    
    def tearDown(self):
        self.client.force_authenticate(user=None)
    
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

    def test_get_members_from_company_returns_200_with_authenticated_user(self):
        response = self.client.get(self.company_members_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_members_from_company_returns_401_if_user_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.company_members_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_members_from_company_returns_only_members_from_company(self):
        response = self.client.get(self.company_members_url, format='json')
        self.assertEqual(len(response.data), 1)
    
    def test_registry_member_in_company_returns_200_with_authenticated_user(self):
        data = {
            'user_id': self.another_user.id,
            'company_id': self.company_django.id
        }
        response = self.client.post(self.registry_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_registry_member_in_company_returns_401_if_user_not_authenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'user_id': self.another_user.id,
            'company_id': self.company_django.id
        }
        response = self.client.post(self.registry_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_registry_member_in_company_returns_400_if_user_id_is_empty(self):
        data = {
            'user_id': '',
            'company_id': self.company_django.id
        }
        response = self.client.post(self.registry_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registry_member_in_company_returns_400_if_company_id_is_empty(self):
        data = {
            'user_id': self.another_user.id,
            'company_id': ''
        }
        response = self.client.post(self.registry_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_registry_member_in_company_returns_404_if_user_doesnt_exist(self):
        data = {
            'user_id': 100,
            'company_id': self.company_django.id
        }
        response = self.client.post(self.registry_member_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_registry_member_in_company_add_user_to_company(self):
        data = {
            'user_id': self.another_user.id,
            'company_id': self.company_django.id
        }
        qty_users_before_post = self.company_django.user.all().count()
        self.client.post(self.registry_member_url, data, format='json')
        self.assertNotEqual(self.company_django.user.all().count(), qty_users_before_post)
    

class CompanyExternalDataTest(APITestCase):
    def test_get_company_external_data_returns_right_keys(self):
        with patch('restapi.views.requests.get') as mock_get:
            expected_values = {
                'nome': 'company LTDA',
                'fantasia': 'company',
                'situacao': 'Ativa',
                'cnpj': '99315678901234',
                'data_situacao': '2019-01-01',
                'uf': 'SP',
            }

            mock_get.return_value = Mock(status_code=200)
            mock_get.return_value.json.return_value = expected_values
            response = get_company_data_from_external_api('12345678901234')

        self.assertEqual(set(response.keys()), set({'nome', 'fantasia', 'situacao'}))