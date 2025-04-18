from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from Authentication_Api.serializers import UserSerializer
from Authentication_Api.models import UserRegistration
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.permissions import AllowAny
# Create your views here.


@api_view(['GET'])
def greet(request):
    return HttpResponse('<h1>welcome to our page</h1>')

class Registration(ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User is created successfully',
                             'status': 201}, status=status.HTTP_201_CREATED)
        return Response({'message': 'User creation failed',
                         'errors': serializer.errors,
                         'status': 400}, status=status.HTTP_400_BAD_REQUEST)


class Login(ViewSet):
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password)

        if email is None or password is None:
            return Response({
                'error': 'Email and password are required',
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is None:
            return Response({
                'error': 'Invalid email or password',
            }, status=status.HTTP_400_BAD_REQUEST)

        access_token = AccessToken.for_user(user)

        return Response({
            'access': str(access_token),
            'name': user.name,
            'email': user.email,
        }, status=status.HTTP_200_OK)
