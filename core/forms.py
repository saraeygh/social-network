from django import forms


class SearchUserForm(forms.Form):
    username = forms.CharField(required=True)