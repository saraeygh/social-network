from django.contrib import admin
from django.urls import path
from .views import Users, UserProfile

urlpatterns = [
    path('', Users.as_view(), name='Users'),
    path('<str:username>/', UserProfile.as_view(), name='UserProfile'),
]