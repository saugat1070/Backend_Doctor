from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
def greet(request):
    return HttpResponse('<h1>welcome to our page</h1>')
