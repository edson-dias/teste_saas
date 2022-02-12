from django.db import IntegrityError
from django.test import TestCase
from ..models import User, Company

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_name = 'django'
        cls.last_name = 'framework'
        cls.email = 'django_framework@outlook.com'
        cls.password = '123456'
        User.objects.create_user(
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=cls.email,
            password=cls.password
        )

    def test_user_str_returns_full_name(self):
        user = User.objects.get(id=2)
        self.assertEqual(str(user), 'django framework')

    def test_user_first_name_equals_django(self):
        user = User.objects.get(id=2)
        self.assertEqual(user.first_name, 'django')
    
    def test_user_last_name_equals_framework(self):
        user = User.objects.get(id=2)
        self.assertEqual(user.last_name, 'framework')
    
    def test_user_email_equals_django_framework(self):
        user = User.objects.get(id=2)
        self.assertEqual(user.email, 'django_framework@outlook.com')

    def test_is_user_valid_fails_if_first_name_is_none(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                first_name=None,
                last_name=self.last_name,
                email=self.email,
                password=self.password
            )               
            
    def test_is_user_valid_fails_if_last_name_is_none(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                first_name=self.first_name,
                last_name=None,
                email=self.email,
                password=self.password
            )
    
    def test_is_user_valid_fails_if_email_is_none(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                first_name=self.first_name,
                last_name=self.last_name,
                email=None,
                password=self.password
            )
    
    def test_is_user_valid_fails_if_password_is_none(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                password=None
            )
    
    def test_create_user_fails_if_email_is_not_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                password=self.password
            )
            
    def test_create_superuser_fails_if_email_is_not_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                password=self.password
            )


class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            first_name='django',
            last_name='framework',
            email='django_framework@outlook.com',
            password='1234ff56'
        )
        company = Company(
            corporate_name='EC LTDA',
            trade_name='EC',
            cnpj='12345678901234',
        )
        company.save()
        company.user.add(user)
        cls.company = Company.objects.get(id=1)
        

    def test_company_corporate_name_equals_ec_ltda(self):
        self.assertEqual(self.company.corporate_name, 'EC LTDA')
    
    def test_company_trade_name_equals_ec(self):
        self.assertEqual(self.company.trade_name, 'EC')
    
    def test_company_cnpj_equals_12345678901234(self):
        self.assertEqual(self.company.cnpj, '12345678901234')
    
    def test_company_user_equals_django_framework(self):
        user = self.company.user.values().first()
        user_full_name = f"{user['first_name']} {user['last_name']}"
        self.assertEqual(user_full_name, str(User.objects.get(id=1)))
    
    def test_create_company_fails_if_cnpj_is_not_unique(self):
        company = Company(
            corporate_name='ECC LTDA',
            trade_name='ECA',
            cnpj='12345678901234'
        )
        with self.assertRaises(IntegrityError):
            company.save()
    
    def test_cnpj_max_length_is_14(self):
        max_length = self.company._meta.get_field('cnpj').max_length
        self.assertEqual(max_length, 14)
    
    def test_company_str_returns_corporate_name(self):
        self.assertEqual(str(self.company), 'EC LTDA')