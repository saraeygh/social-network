from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from reaction.models import Reaction
from .forms import PostForm, ImageFormSet
from .models import Post, Image
from django.utils.text import slugify


class NewPost(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm(
            initial={
                'user': request.user,
                'post_slug': 'slug',
            }
        )
        context = {'form': form}
        return render(request, 'new_post.html', context)
    
    def post(self, request):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.cleaned_data
            title = form['title']
            content = form['content']
            post_slug = slugify(form['title'])
            user = form['user']
            
            new_post = Post.objects.create(
                title=title,
                content=content,
                post_slug=post_slug,
                user=user,
            )

            new_post.save()

            username = request.user
            return redirect('useraccounts:userprofile', username)
        
        else:
            errors = form.errors
            form = PostForm()
            context = {
                'form': form,
                'errors': errors,
                }
            return render(request, 'new_post.html', context)


class EditPost(LoginRequiredMixin, View):
    
    def get(self, request, id):
        edit_post = Post.objects.get(id=id)
        
        if request.user == edit_post.user:

            form = PostForm(
                initial={
                    'title': edit_post.title,
                    'content': edit_post.content,
                    'user': edit_post.user,
                    'post_slug': edit_post.post_slug,
                }
            )
            context = {'form': form}
            return render(request, 'new_post.html', context)
        else:
            return redirect(
                request.META.get('HTTP_REFERER', 'core:landing')
                )
        
    def post(self, request, id):
        edited_post = Post.objects.get(id=id)
        form = PostForm(request.POST, request.FILES, instance=edited_post)

        if form.is_valid():
            form.save()

            username = request.user
            return redirect('useraccounts:userprofile', username)
        
        else:
            errors = form.errors
            form = PostForm()
            context = {
                'form': form,
                'errors': errors,
                }
            return render(request, 'new_post.html', context)


class DeletePost(LoginRequiredMixin, View):
    
    def get(self, request, id):
        edit_post = Post.objects.get(id=id)
        
        if request.user == edit_post.user:
            edit_post.delete()
            return redirect(request, 'useraccounts:userprofile', request.user.username)
        else:
            return redirect(
                request.META.get('HTTP_REFERER', 'core:landing')
                )


class LikePost(LoginRequiredMixin, View):

    def get(self, request, id):

        REACTION_FOR_ID = 8
        REACTION_FROM_ID = 1
        
        reaction_status = "LIKE"
        object_id = id
        user = request.user.id

        is_liked = Reaction.objects.filter(object_id=id).filter(reaction_status=reaction_status).filter(user=user)

        if is_liked.exists():
            is_liked.delete()
            return redirect(
                request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
                )

        new_reaction = Reaction(
            reaction_status=reaction_status,
            object_id=object_id,
            user=user,
            reaction_for_id=REACTION_FOR_ID,
            reaction_from_id=REACTION_FROM_ID,
        )
        new_reaction.save()
        return redirect(
            request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            )


class DislikePost(LoginRequiredMixin, View):

    def get(self, request, id):

        REACTION_FOR_ID = 8
        REACTION_FROM_ID = 1
        
        reaction_status = "DISLIKE"
        object_id = id
        user = request.user.id

        is_liked = Reaction.objects.filter(object_id=id).filter(reaction_status=reaction_status).filter(user=user)

        if is_liked.exists():
            is_liked.delete()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        
        new_reaction = Reaction(
            reaction_status=reaction_status,
            object_id=object_id,
            user=user,
            reaction_for_id=REACTION_FOR_ID,
            reaction_from_id=REACTION_FROM_ID,
        )
        new_reaction.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class SinglePost(View):

    def get(self, request, post_slug):
        single_post = Post.objects.filter(post_slug=post_slug)

        context = {
            "single_post": single_post,
        }

        return render(request, 'singlepost.html', context)
