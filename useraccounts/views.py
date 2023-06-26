from django.shortcuts import render
from django.views import View
from .models import UserAccount
from posts.models import Post


class Users(View):
    def get(self, request):
        users = UserAccount.objects.filter(soft_delete=False)
        return render(request, 'users.html', {'users': users })
    

class UserProfile(View):
    def get(self, request, username):
        user = UserAccount.objects.get(username=username)
        user_posts = Post.objects.filter(user=user.id)
        return render(request, 'userprofile.html', {'user': user, 'user_posts': user_posts })