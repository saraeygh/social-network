from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.views import View
from posts.models import Post
from useraccounts.models import UserAccount


class LandingPageView(View):

    def get(self, request):
        posts_list = Post.objects.all()
        users_list = UserAccount.objects.all()

        search_username = request.GET.get('username')

        context = {
                    'users_list': users_list,
                    'posts_list': posts_list,
                    'user': request.user,
                }

        if search_username is None or search_username == '':
            return render(request, 'landing.html', context)
        
        return redirect(f"useraccounts/search/?username={search_username}")
        
