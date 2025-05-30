from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from Authentication_Api.serializers import UserSerializer
from Authentication_Api.models import UserRegistration
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action

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
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


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
        
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
        
@action(detail=False,methods=['get'],url_path='profile')        
class Profile(ViewSet):
    def retrieve(self, request, pk=None):
        print("i am here")
        user = request.user  
        print(user)
        if not user.is_authenticated:
            return Response({
                'message': 'Authentication credentials were not provided or invalid.',
                'status': 401
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        return Response({
            'message': 'Successful',
            'data': serializer.data,
            'status': 200
        }, status=status.HTTP_200_OK)
        
        
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
@action(detail=False,methods=['put'],url_path='profile_update')
class Profile_update(ViewSet):
    
    def update(self,request,pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data,partial=True)
        if not user.is_authenticated:
            return Response({
                "message":"Unauthorized user",
            })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':"update succes",
                'status':202,
                'data':serializer.data
            },status=status.HTTP_202_ACCEPTED)
        return Response({
            'message':"Bad request",
            'status':400
        },status=status.HTTP_400_BAD_REQUEST)
        
    
    def get_permission(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    
