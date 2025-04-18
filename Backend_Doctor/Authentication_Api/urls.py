
from django.urls import path,include
from Authentication_Api import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'register', views.Registration, basename='register')
router.register(r'login', views.Login, basename='loign')

urlpatterns = router.urls
