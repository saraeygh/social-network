from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import UserAccount


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'password1', 'password2']


class SignInForm(forms.Form):

    username = forms.CharField(
        required=True,
        label=_("Username")
        )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label=_("Password")
        )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
        ]

        labels = {
            'image': 'Profile picture',
        }
