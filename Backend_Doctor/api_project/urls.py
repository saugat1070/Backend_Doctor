
from django.urls import path,include
from api_project import views

urlpatterns = [
   path('',views.greet,name='greet'),
   
]