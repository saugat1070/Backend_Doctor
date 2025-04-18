from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from Authentication_Api.models import UserRegistration
class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        print(email,password)
        try:
            user = UserRegistration.objects.get(email=email)
            print(user)
            if user.check_password(password):
                return user
        
        except UserRegistration.DoesNotExist:
            return None
        