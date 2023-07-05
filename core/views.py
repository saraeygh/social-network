from django.shortcuts import render
from django.views import View
from posts.models import Post
from useraccounts.models import UserAccount
from reaction.models import Reaction


class LandingPageView(View):

    def get(self, request):
        posts_list = Post.objects.all()
        users_list = UserAccount.objects.all()
        reactions = Reaction.objects.all()

        for post in posts_list:
            post.likes = Reaction.objects.filter(object_id=post.id).filter(reaction_status='LIKE').count()
            post.dislikes = Reaction.objects.filter(object_id=post.id).filter(reaction_status='DISLIKE').count()
            post.save()

        return render(
            request,
            'landing.html', 
            {
                'users_list': users_list,
                'posts_list': posts_list,
                'user': request.user,
            }
            )
