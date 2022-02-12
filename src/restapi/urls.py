from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
#router.register(r'company', CompanyViewSet)
api_urls = router.urls