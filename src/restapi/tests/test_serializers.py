from django.test import TestCase

from ..models import User, BaseUser, Company
from ..serializers import UserSerializer


class UserSerializersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        base_user = BaseUser(
            first_name='django',
            last_name='framework',
            email='django_framework@gmail.com',
            password='654321'
        )
                
        User.objects.create_user(base_user)
        cls.user = User.objects.first()

        company = Company(
            corporate_name='EC LTDA',
            trade_name='EC',
            cnpj='12345678901234',
        )
        company.save()
        company.user.add(cls.user)
        
        cls.company = Company.objects.first()
        cls.user_serializer = UserSerializer(instance=cls.user)
        

    def test_user_serializer_contains_expected_fields(self):
        keys = self.user_serializer.data.keys()
        expected_keys = ['id', 'first_name', 'last_name', 'email']
        self.assertEqual(set(keys), set(expected_keys))
    
    def test_user_serializer_contains_expected_data(self):
        data = self.user_serializer.data
        self.assertEqual(data['first_name'], 'django')
    
    def test_user_serializer_can_deserialize_user(self):
        data = {
            'first_name': 'new_django',
            'last_name': 'framework',
            'email': 'new_django@hotmail.com',
            'password': '123456789'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_can_create_user(self):
        data = {
            'first_name': 'new_django',
            'last_name': 'framework',
            'email': 'new_django@hotmail.com',
            'password': '123456789'
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(User.objects.count(), 2)
    
    def test_user_serializer_can_update_user(self):
        data = {
            'first_name': 'new_django',
            'last_name': 'framework',
            'email': 'new_email@gmail.com',
            'password': '123456789'
        }
        serializer = UserSerializer(data=data, instance=self.user)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'new_email@gmail.com')

    def test_user_serializer_crypt_password(self):
        data = {
            'first_name': 'new_django',
            'last_name': 'framework',
            'email': 'new_email@gmail.com',
            'password': '123456789'
        }
        serializer = UserSerializer(data=data, instance=self.user)
        if serializer.is_valid():
            serializer.save()
        self.assertNotEqual(User.objects.first().password, '123456789')
