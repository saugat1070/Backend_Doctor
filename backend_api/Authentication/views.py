from django.shortcuts import render
from Authentication.serializer import SignUp as SignUpSerializer, Profile
from Authentication.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from Authentication.serializer import Profile as ProfileSerializer
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

