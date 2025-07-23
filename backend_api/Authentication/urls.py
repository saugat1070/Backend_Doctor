from django.urls import path
from Authentication import views


urlpatterns = [
    path('create', views.SignUp.as_view() , name="register"),
    path("signin",views.SignIn.as_view(),name="signin"),
    path("profile",views.profile_fetch.as_view(),name="profile_fetch")
    
]

