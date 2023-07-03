from django.contrib import admin
from django.urls import path
from .views import ShowPosts

app_name = "posts"
urlpatterns = [
    path('', ShowPosts.as_view(), name='ShowPosts'),
]