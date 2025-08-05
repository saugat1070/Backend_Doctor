from django.shortcuts import render,redirect
from Authentication.serializer import SignUp as SignUpSerializer, Profile
from Authentication.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from Authentication.serializer import Profile as ProfileSerializer
import os
from dotenv import load_dotenv

load_dotenv()
import requests
# Create your views here.

class SignUp(APIView):
    
    def post(self, request, format=None):
        print(request.data)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return JsonResponse({
                "message" : "User created Successfully",
                "data" : serializer.data
                }, status=status.HTTP_201_CREATED)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request,*args):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email,password)
        if not email or not password:
            return JsonResponse({
                "message": "Email and password should be provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            find_user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'message': "User with this email is not found"
            }, status=status.HTTP_404_NOT_FOUND)
        print(find_user)
        user = authenticate(request, email=email, password=password)
        print(user)
        if not user:
            return JsonResponse({
                "message": "Please enter correct email and password" 
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        token = AccessToken.for_user(user)
        print(token)
        return JsonResponse({
            "message": "Login successful",
            "data": {
                "access_token": str(token)
            }
        }, status=status.HTTP_200_OK)
        
class profile_fetch(APIView):
    def get(self, request):
        print(request.user)
        if request.user.is_authenticated == True:
            profile_serializer = ProfileSerializer(request.user)
            if not profile_serializer:
                return JsonResponse({
                    "message":"something is wrong during finding details in Database"
                })
            return JsonResponse({
                "message" : "profile fetch successfull",
                "data" : profile_serializer.data
            })
        return JsonResponse({
            "message" : "user must be login first"
        })
        
    def patch(self,request):
        if request.user.is_authenticated:
            instance = User.objects.get(pk=request.user.id)
            serializer = ProfileSerializer(instance,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "message" : "profile update successfully"
                })
            return JsonResponse({
                "message" : "something is wrong"
            })
        return JsonResponse({
            "message":"please login first"
        })


class GoogleAuthentication(APIView):
    permission_classes = [AllowAny]
    def __init__(self):
        self.google_client_secret_key = os.getenv("GoogleClientSecretKey")
        self.google_client_id = os.getenv("GoogleClientId")
        self.redirect_url = os.getenv("RedirectUrl")
        print(self.google_client_id,self.google_client_secret_key,self.redirect_url)
    def get(self,request):
        auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={self.google_client_id}&redirect_uri={self.redirect_url}&scope=profile%20email'
        return redirect(auth_url)
    
    
class GoogleCallback(APIView):
    permission_classes = [AllowAny]

    def __init__(self):
        self.google_client_secret_key = os.getenv("GoogleClientSecretKey")
        self.google_client_id = os.getenv("GoogleClientId")
        self.redirect_url = os.getenv("RedirectUrl")
        print(self.google_client_id, self.google_client_secret_key, self.redirect_url)
        
    def get(self,request):
        code = request.GET.get("code")
        try:
            tokenResponse = requests.post(
                f'https://oauth2.googleapis.com/token',
                json={
                    "code":code,
                    "client_id": self.google_client_id,
                    "client_secret": self.google_client_secret_key,
                    "redirect_uri": self.redirect_url,
                    "grant_type": 'authorization_code'
                }
            )
            print(tokenResponse)
            token_data = tokenResponse.json()
            accessToken = token_data.get("access_token")
            
            userRes = requests.get(
                f'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={
                    "Authorization": f'Bearer {accessToken}'
                }
            )
            
            return JsonResponse({
                "data": userRes.json()
            })
        except Exception as e:
            return JsonResponse({
                "message": "An error occurred during Google callback",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
    
        
        