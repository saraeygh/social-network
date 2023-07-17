from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.views import View

from posts.models import Post
from useraccounts.models import UserAccount


class LandingPageView(View):

    def setup(self, request, *args, **kwargs):
        self.posts_list = Post.objects.all()
        self.users_list = UserAccount.objects.all()
        self.search_username = request.GET.get("username")
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        context = {
                    'users_list': self.users_list,
                    'posts_list': self.posts_list,
                    'user': request.user,
                }

        if self.search_username is None or self.search_username == '':
            return render(request, 'landing.html', context)

        return redirect(
            f"useraccounts/search/?username={self.search_username}"
            )
