from django.shortcuts import render
from django.views import View
from .models import Post


class ShowPosts(View):
    def get(self, request):
        posts_list = Post.objects.all()
        return render(request, 'posts.html', {'posts_list': posts_list, 'host': request.get_host()})