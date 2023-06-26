from django.contrib import admin
from django.urls import path
from .views import ShowPosts

urlpatterns = [
    path('', ShowPosts.as_view(), name='ShowPosts'),
]