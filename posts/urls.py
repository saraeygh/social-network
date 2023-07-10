from django.urls import path
from .views import (
    NewPost,
    EditPost,
    DeletePost,
    LikePost,
    DislikePost,
    SinglePost,
    DeletePostImage,
)

app_name = 'posts'
urlpatterns = [
    path('<int:id>/like', LikePost.as_view(), name='signup'),
    path('<int:id>/dislike', DislikePost.as_view(), name='signup'),
    # **************************************************************
    path('newpost/', NewPost.as_view(), name='newpost'),
    path('editpost/<int:id>/', EditPost.as_view(), name='editpost'),
    path('editpost/<int:id>/delete/<int:image_id>', DeletePostImage.as_view(), name='deletepostimage'),
    path('editpost/<int:id>/delete', DeletePost.as_view(), name='deletepost'),
    path('post/<int:id>/<str:post_slug>/', SinglePost.as_view(), name='singlepost'),
]