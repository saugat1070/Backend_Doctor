from django.shortcuts import redirect
from Authentication.serializer import Profile, CreateUserSerializer
from Authentication.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from Authentication.serializer import Profile as ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import threading
import random
import requests
import os

class GoogleAuthentication(APIView):
    permission_classes = [AllowAny]

    def __init__(self):
        self.google_client_secret_key = os.getenv("GoogleClientSecretKey")
        self.google_client_id = os.getenv("GoogleClientId")
        self.redirect_url = os.getenv("RedirectUrl")

    def get(self, request):
        auth_url = (
            'https://accounts.google.com/o/oauth2/v2/auth'
            f'?response_type=code&client_id={self.google_client_id}'
            f'&redirect_uri={self.redirect_url}&scope=profile%20email'
        )
        return redirect(auth_url)


class GoogleCallback(APIView):
    permission_classes = [AllowAny]

    def __init__(self):
        self.google_client_secret_key = os.getenv("GoogleClientSecretKey")
        self.google_client_id = os.getenv("GoogleClientId")
        self.redirect_url = os.getenv("RedirectUrl")

    def get(self, request):
        code = request.GET.get("code")
        try:
            tokenResponse = requests.post(
                'https://oauth2.googleapis.com/token',
                json={
                    "code": code,
                    "client_id": self.google_client_id,
                    "client_secret": self.google_client_secret_key,
                    "redirect_uri": self.redirect_url,
                    "grant_type": 'authorization_code',
                },
                timeout=20,
            )
            token_data = tokenResponse.json()
            accessToken = token_data.get("access_token")

            userRes = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={"Authorization": f'Bearer {accessToken}'},
                timeout=20,
            )

            return JsonResponse({"data": userRes.json()})
        except Exception as e:
            return JsonResponse({"message": "An error occurred during Google callback", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        fullName = data.get('fullName')
        if not email or not password or not fullName:
            return JsonResponse({'message': 'Please provide email,password and fullName'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateUserSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
        except Exception:
            return JsonResponse({'message': 'error in database creation'}, status=status.HTTP_403_FORBIDDEN)

        return JsonResponse({'message': 'User is created Successfully!!'}, status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return JsonResponse({'message': 'please enter email and password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user with this email  is not found!!'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return JsonResponse({'message': 'bad request,please send again'}, status=status.HTTP_400_BAD_REQUEST)

        token = AccessToken.for_user(user)
        return JsonResponse({'message': 'Login successful', 'token': str(token)}, status=status.HTTP_200_OK)


class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return JsonResponse({'message': "couldn't find user id"}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES.get('file') or request.FILES.get('image')
        image_url = request.data.get('imageUrl')
        photo_value = image_file or image_url or 'https://localhost:3000/profile.png'

        try:
            instance = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User is not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'email' in request.data:
            instance.email = request.data.get('email')
        if 'role' in request.data:
            instance.role = request.data.get('role')
        if 'dob' in request.data:
            instance.date_of_birth = request.data.get('dob')
        if photo_value:
            instance.photo_name = photo_value

        try:
            instance.save()
            return JsonResponse({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'message': 'Something wrong in update'}, status=status.HTTP_403_FORBIDDEN)


class FetchUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return JsonResponse({'message': 'User is not found!,please provide valid token'}, status=status.HTTP_404_NOT_FOUND)
        data = ProfileSerializer(user).data
        return JsonResponse({'message': 'User information fetch successfully', 'data': data}, status=status.HTTP_200_OK)


def generate_otp(length: int = 6) -> str:
    digits = '0123456789'
    return ''.join(random.choice(digits) for _ in range(length))


class ForgetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user with this email is not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp(6)
        try:
            user.otp = otp
            user.save()
            # TODO: sendMail equivalent here
            def clear_otp(u_id):
                try:
                    u = User.objects.get(id=u_id)
                    u.otp = ''
                    u.save()
                except Exception:
                    pass
            threading.Timer(60.0, clear_otp, args=[user.id]).start()
        except Exception:
            pass

        return JsonResponse({'message': 'message is send in your mail'}, status=status.HTTP_200_OK)


class VerifyOtp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return JsonResponse({'message': 'email and otp should be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user with this email is not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            return JsonResponse({'message': 'otp is verified'}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'otp is not verified!!'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        confirmPassword = request.data.get('confirmPassword')
        newPassword = request.data.get('newPassword')
        if not email or not confirmPassword or not newPassword:
            return JsonResponse({'message': 'please provide email and password'}, status=status.HTTP_400_BAD_REQUEST)
        if newPassword != confirmPassword:
            return JsonResponse({'message': 'newPassword and confirm password should be same'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'message': 'user with this email is not found!!'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user.set_password(newPassword)
            user.save()
            return JsonResponse({'message': 'password change successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'message': 'Something wrong in update'}, status=status.HTTP_403_FORBIDDEN)




