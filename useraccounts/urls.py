from django.urls import path
from .views import UserProfile, SignUp, SignIn

app_name = "useraccounts"
urlpatterns = [
    path('username/<str:username>/', UserProfile.as_view(), name='userprofile'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
]