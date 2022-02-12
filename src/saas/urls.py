from django.contrib import admin
from django.urls import path, include
from restapi.urls import api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_urls)),
]
