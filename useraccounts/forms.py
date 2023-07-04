from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm  
from .models import UserAccount


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=150, required=False, help_text="Optional")
    first_name = forms.CharField(max_length=150, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=150, required=False, help_text="Optional")
    bio = forms.CharField(max_length=255, required=False, help_text="Optional")
    profile_image = forms.FileField(required=False, help_text="Optional")

    
    def check_username(self, username: str):
        all_users = UserAccount.objects_all.values_list(flat=True)
        if not username in all_users:
            return username
        else:
            # Error if username already exists
            pass

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'password1',
            'password2',
        ]

class SignInForm(forms.Form):

    username = forms.CharField(
        required=True,
        )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True
        )
    
    
class EditProfileForm(forms.ModelForm):

    new_password = forms.CharField(
        max_length=128,
        required=False,
        help_text='* - At least 8, numbers & letters, not common passwords',
        )
    
    confirm_new_password = forms.CharField(
        max_length=128,
        required=False,
        help_text='* - Repeat new password',
        )


    class Meta:
        model = UserAccount
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
            'password',
            'new_password',
            'confirm_new_password',
        ]

        widgets = {
            'password': forms.PasswordInput,
            'new_password': forms.PasswordInput,
            'confirm_new_password': forms.PasswordInput,
        }

        labels = {
            'bio': 'Bio',
            'image': 'Profile picture',
            'password': 'Old password',
        }

        help_texts = {
            'username': '* - Unique, 150 characters max (including Letters, digits and @/./+/-/_ only).',
            'email': 'Optional',
            'first_name': 'Optional',
            'last_name': 'Optional',
            'bio': 'Optional',
        }