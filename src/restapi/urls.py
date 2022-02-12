from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from .views import UserViewSet, CompanyViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'company', CompanyViewSet, basename='company')

api_urls = [
    path('api/', include(router.urls)),
    path('api/login', obtain_auth_token, name='api_login'),
]



