from django.urls import path
from .views import UserProfile, SignUp, SignIn, EditUserProfile

app_name = "useraccounts"
urlpatterns = [
    path('username/<str:username>/', UserProfile.as_view(), name='userprofile'),
    
    path(
        'username/<str:username>/edit',
        EditUserProfile.as_view(),
        name='edituserprofile'),
    
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
]