
from django.urls import path
from Authentication_Api import views
# from Authentication_Api.views import Profile_update

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'register', views.Registration, basename='register')
router.register(r'login', views.Login, basename='loign')
# router.register(r'profile',views.Profile, basename='profile')

urlpatterns = [
    path('profile/',views.Profile.as_view({'get':'retrieve'}),name='profile'),
    path('profile_update/',views.Profile_update.as_view({'put':'update'}))
]
urlpatterns += router.urls
