from django.urls import path
from .views import LikePost, DislikePost

app_name = "posts"
urlpatterns = [
    path('<int:id>/like', LikePost.as_view(), name='signup'),
    path('<int:id>/dislike', DislikePost.as_view(), name='signup'),
]