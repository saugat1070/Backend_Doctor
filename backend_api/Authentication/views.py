from django.shortcuts import render
from Authentication.serializer import SignUp as SignUpSerializer, Profile
from Authentication.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
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
    
    def post(self, request,*args):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email,password)
        find_user = User.objects.get(email = email)
        if not find_user:
            return JsonResponse({
                'message' : "user with this email is not found"
            })
        if not email or not password:
            return JsonResponse({
                "message": "Email and password should be provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        print(user)
        if not user:
            return JsonResponse({
                "message": "Please enter correct email and password" 
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        refresh = AccessToken.for_user(user)
        
        return JsonResponse({
            "message": "Login successful",
            "data": {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        }, status=status.HTTP_200_OK)
             
        
