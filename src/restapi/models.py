from dataclasses import dataclass

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


@dataclass
class BaseUser:
    first_name: str
    last_name: str
    email: str
    password: str


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, user, **extra_fields):
        email = self.normalize_email(user.email)
        user = self.model(
            first_name=user.first_name, 
            last_name=user.last_name, 
            email=email, 
            username=user.email, 
            **extra_fields
        )
        user.set_password(user.password)
        user.save(using=self._db)
        return user

    def create_user(self, user, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        if self.is_user_valid(user):
            return self._create_user(user, **extra_fields)

    def create_superuser(self, user, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if self.is_user_valid(user):
            return self._create_user(user, **extra_fields)

    def is_user_valid(self, user):
        if user.first_name is None:
            raise TypeError("first_name is required")
        elif user.last_name is None:
            raise TypeError("last_name is required")
        elif user.email is None:
            raise TypeError("email is required")
        elif user.password is None:
            raise TypeError("password is required")
        else:
            return True


class User(AbstractUser):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField('e-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Company(models.Model):
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    corporate_name = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.corporate_name
        