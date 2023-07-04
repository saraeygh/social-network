from django.urls import path
from .views import (
    UserProfile,
    SignUp,
    SignIn,
    EditUserProfile,
    DeleteAccount,
    SignOut
    )

app_name = "useraccounts"
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signout', SignOut.as_view(), name='signout'),

    path(
        'username/<str:username>/',
        UserProfile.as_view(), 
        name='userprofile'
        ),

    path(
        'username/<str:username>/edit',
        EditUserProfile.as_view(),
        name='edituserprofile'
        ),

    path(
        'username/<str:username>/delete-account',
        DeleteAccount.as_view(), 
        name='deleteuser'
        ),
]
