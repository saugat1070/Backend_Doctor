from django.urls import path
from Authentication import views


urlpatterns = [
    path('create-user', views.CreateUser.as_view(), name='create_user'),
    path('login', views.Login.as_view(), name='login'),
    path('update', views.UpdateUser.as_view(), name='update_user'),
    path('fetch', views.FetchUser.as_view(), name='fetch_user'),
    path('forget', views.ForgetPassword.as_view(), name='forget_password'),
    path('verify-otp', views.VerifyOtp.as_view(), name='verify_otp'),
    path('reset-password', views.ResetPassword.as_view(), name='reset_password'),
    path("auth/google",views.GoogleAuthentication.as_view(),name="googleauth"),
    path("auth/google/callback",views.GoogleCallback.as_view(),name="google_callback")  
]

