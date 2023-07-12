from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from reaction.models import Reaction
from .forms import PostForm, ReplyFrom, TagFormset, ImageFormSet
from .models import Post, Reply, Image
from tags.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

import inspect 


class NewPost(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm(
            initial={
                'user': request.user,
                'post_slug': 'slug',
            }
        )
        tag_formset = TagFormset()
        formset = ImageFormSet()
        
        context = {
            'form': form,
            'formset': formset,
            'tag_formset': tag_formset,
            }
        return render(request, 'new_post.html', context)
    
    def post(self, request):
        form = PostForm(request.POST, instance=Post())
        tag_formset = TagFormset(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid() and tag_formset.is_valid():

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
            
            tag_formset = tag_formset.cleaned_data
            for tag in tag_formset:
                if tag:
                    tag_label = tag['label']

                    new_tag = Tag.objects.update_or_create(
                        label=tag_label,
                    )
                    new_tag[0].save()
                    TaggedItem.add_tagged_item(
                        self=self,
                        tag=new_tag[0],
                        user_id=user.id,
                        post_id=new_post.id,
                        )

            formset = formset.cleaned_data
            for image in formset:
                if image:
                    uoloaded_image = image['image']
                    post_id = new_post

                    new_iamge = Image.objects.create(
                        image=uoloaded_image,
                        post_id=post_id,
                    )
                    new_iamge.save()

            username = request.user
            return redirect('useraccounts:userprofile', username)
        
        else:
            errors = form.errors
            form = PostForm()
            formset = ImageFormSet()
            context = {
                'form': form,
                'formset': formset,
                'errors': errors,
                }
            return render(request, 'new_post.html', context)


class EditPost(LoginRequiredMixin, View):
    
    def get(self, request, id):
        edit_post = Post.objects.get(id=id)
        post_tags = TaggedItem.objects.filter(object_id=id)
        
        if request.user.id == edit_post.user.id:

            form = PostForm(
                initial={
                    'title': edit_post.title,
                    'content': edit_post.content,
                    'user': edit_post.user,
                    'post_slug': edit_post.post_slug,
                }
            )
            tag_formset = TagFormset()
            formset = ImageFormSet()

            context = {
                'edit_post': edit_post,
                'post_tags': post_tags,
                'tag_formset': tag_formset,
                'formset': formset,
                'form': form,
                }
            
            return render(request, 'edit_post.html', context)
        
        return redirect('useraccounts:signin')
        
    def post(self, request, id):
        edited_post = Post.objects.get(id=id)
        form = PostForm(request.POST, instance=edited_post)
        formset = ImageFormSet(request.POST, request.FILES)
        tag_formset = TagFormset(request.POST)

        if form.is_valid() and formset.is_valid() and tag_formset.is_valid():
            form.save()

            formset = formset.cleaned_data
            for image in formset:
                if image:
                    uoloaded_image = image['image']
                    post_id = edited_post

                    new_iamge = Image.objects.create(
                        image=uoloaded_image,
                        post_id=post_id,
                    )
                    new_iamge.save()
            
            tag_formset = tag_formset.cleaned_data
            for tag in tag_formset:
                if tag:
                    tag_label = tag['label']

                    new_tag = Tag.objects.update_or_create(
                        label=tag_label,
                    )
                    new_tag[0].save()
                    
                    TaggedItem.add_tagged_item(
                        self=self,
                        tag=new_tag[0],
                        user_id=request.user.id,
                        post_id=edited_post.id,
                        )

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
        post = Post.objects.get(id=id)
        
        if request.user.id == post.user.id:
            post.delete_post()
            return redirect('useraccounts:userprofile', request.user.username)
        
        return redirect('useraccounts:signin')
    

class DeletePostTag(LoginRequiredMixin, View):
    
    def get(self, request, id, tag_id):
        post = Post.objects.get(id=id)
        tag = TaggedItem.objects.get(id=tag_id)
        
        if request.user.id == post.user.id:
            tag.delete()
            return redirect('posts:editpost', post.id)
        
        return redirect('useraccounts:signin')


class DeletePostImage(LoginRequiredMixin, View):
    
    def get(self, request, id, image_id):
        post = Post.objects.get(id=id)
        image = Image.objects.get(id=image_id)
        
        if request.user.id == post.user.id:
            image.delete()
            return redirect('posts:editpost', post.id)
        
        return redirect('useraccounts:signin')


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

    def get(self, request, id, post_slug):
        single_post = Post.objects.filter(id=id)
        
        reply_form = ReplyFrom(
            initial={
                    'user': request.user,
                    'post_id': list(single_post)[0],
                }
        )

        context = {
            "single_post": single_post,
            'reply_form': reply_form,
        }

        return render(request, 'singlepost.html', context)
    
    def post(self, request, id, post_slug):
        form = ReplyFrom(request.POST)

        if form.is_valid():
            form = form.cleaned_data

            content = form['content']
            user = form['user']
            post_id = form['post_id']
            reply_id = form['reply_id']
            
            new_reply = Reply.objects.create(
                content=content,
                user=user,
                post_id=post_id,
                reply_id=reply_id,
            )

            new_reply.save()

            return redirect('posts:singlepost', id, post_slug)
        
        else:
            return render(request, 'posts:singlepost', id, post_slug)


class TagPosts(View):

    def get(self, request, tag_id, tag_label):
        
        posts_list = list(TaggedItem.objects.select_related('content_type').filter(tag_id=tag_id).filter(content_type_id=8))
        all_used_tags = TaggedItem.all_used_tags()

        context = {
            "all_used_tags": all_used_tags,
            'posts_list': posts_list,
        }

        return render(request, 'tag_posts.html', context)
