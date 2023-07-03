from django import forms
from .models import UserAccount


class SignUpForm(forms.ModelForm):

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=128,
        required=True,
        help_text='* - Repeat password',
        )

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'password',
            'confirm_password',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
        ]

        widgets = {
            'password': forms.PasswordInput,
            'confirm_password': forms.PasswordInput,
        }

        labels = {
            'bio': 'Bio',
            'image': 'Profile picture',
        }

        help_texts = {
            'username': '* - Unique, 150 characters max (including Letters, digits and @/./+/-/_ only).',
            'password': '* - At least 8, numbers & letters, not common passwords.',
            'email': 'Optional',
            'first_name': 'Optional',
            'last_name': 'Optional',
            'bio': 'Optional',
        }


class SignInForm(forms.Form):

    username = forms.CharField(
        required=True,
        )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True
        )