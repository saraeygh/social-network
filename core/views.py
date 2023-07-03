from django.shortcuts import render
from django.views import View
from posts.models import Post
from useraccounts.models import UserAccount


class LandingPageView(View):
    
    def get(self, request):      
        posts_list = Post.objects.all()
        users_list = UserAccount.objects.all()

        return render(
            request,
            'landing.html', 
            {
                'users_list': users_list,
                'posts_list': posts_list,
                'user': request.user,
                'host': request.get_host()
            }
            )