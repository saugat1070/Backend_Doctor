from django.urls import path
from Authentication import views


urlpatterns = [
    path('create', views.SignUp.as_view() , name="register"),
    path("signin",views.SignIn.as_view(),name="signin")
    
]

