from django.urls import path
from .views import (
    NewPost,
    EditPost,
    DeletePost,
    LikePost,
    DislikePost,
    SinglePost,
    DeletePostTag,
    DeletePostImage,
    TagPosts,
)

app_name = 'posts'

urlpatterns = [
    path('<int:id>/like', LikePost.as_view(), name='like'),
    path('<int:id>/dislike', DislikePost.as_view(), name='dislike'),
    path('newpost/', NewPost.as_view(), name='newpost'),
    path('editpost/<int:id>/', EditPost.as_view(), name='editpost'),
    path('editpost/<int:id>/delete', DeletePost.as_view(), name='deletepost'),

    path(
        'editpost/<int:id>/delete-tag/<int:tag_id>',
        DeletePostTag.as_view(),
        name='deleteposttag'),
    path(
        'editpost/<int:id>/delete-image/<int:image_id>',
        DeletePostImage.as_view(),
        name='deletepostimage'),
    path(
        'post/<int:id>/<str:post_slug>/',
        SinglePost.as_view(),
        name='singlepost'),
    path(
        'tag/<int:tag_id>/<str:tag_label>/',
        TagPosts.as_view(),
        name='tagposts'),
]