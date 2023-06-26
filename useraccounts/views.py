from django.shortcuts import render
from django.views import View
from .models import UserAccount


class Users(View):
    def get(self, request):
        users = UserAccount.objects.filter(soft_delete=False)
        return render(request, 'users.html', {'users': users })
    
class UserProfile(View):
    def get(self, request, username):
        user = UserAccount.objects.filter(username=username).first()
        return render(request, 'userprofile.html', {'users': user })