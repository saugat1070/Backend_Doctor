
from django.contrib import admin
from django.urls import path
from django.urls import include
import Authentication.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/api/",include(Authentication.urls))
]
