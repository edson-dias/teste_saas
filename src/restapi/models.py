from datetime import date

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, first_name, last_name, email, password=None):
        if self._is_user_valid(first_name, last_name, email, password):
            user = self.model(
                first_name=first_name,
                last_name=last_name,
                email=self.normalize_email(email),
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, first_name, last_name, email, password):
        if self._is_user_valid(first_name, last_name, email, password):
            user = self.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.is_admin = True
            user.save(using=self._db)
            return user

    def _is_user_valid(self, first_name, last_name, email, password):
        if first_name is None or last_name is None or email is None or password is None:
            raise TypeError("Arguments can't be None")
        elif first_name == '' or last_name == '' or email == '' or password == '':
            raise TypeError("Arguments can't be empty")
        else:
            return True


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField('e-mail', unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Company(models.Model):
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    corporate_name = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    user = models.ManyToManyField(User, blank=True)
    status = models.CharField(max_length=100, default='Ativa')
    last_check = models.DateTimeField(default=timezone.localtime)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.corporate_name

    @property
    def is_necessary_to_check(self):
        return self.last_check.date() <= (date.today() - relativedelta(months=1))
    
    def update_company(self, corporate_name, trade_name, status):
        self.corporate_name = corporate_name
        self.trade_name = trade_name
        self.status = status
        self.last_check = timezone.localtime()
        self.save()