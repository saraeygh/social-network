from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

from reaction.models import Reaction
from tags.models import Tag, TaggedItem
from .forms import PostForm, ReplyFrom, TagFormset, ImageFormSet
from .models import Post, Image


class NewPost(LoginRequiredMixin, View):

    def get(self, request):
        tag_formset = TagFormset()
        formset = ImageFormSet()

        form = PostForm(
            initial={
                'user': request.user,
                'post_slug': 'slug',
            }
        )

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

            new_post = form.save(commit=False)
            form = form.cleaned_data
            new_post.post_slug = slugify(form['title'])
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
                        user_id=request.user.id,
                        post_id=new_post.id,
                        )

            formset = formset.cleaned_data
            for image in formset:
                if image:
                    uploaded_image = image['image']
                    post_id = new_post

                    new_image = Image.objects.create(
                        image=uploaded_image,
                        post_id=post_id,
                    )
                    new_image.save()

            username = request.user
            return redirect('useraccounts:userprofile', username)

        else:
            errors = form.errors

            tag_formset = TagFormset()
            formset = ImageFormSet()
            form = PostForm(
                initial={
                    'user': request.user,
                    'post_slug': 'slug',
                    }
            )

            context = {
                'errors': errors,
                'tag_formset': tag_formset,
                'formset': formset,
                'form': form,
                }

            return render(request, 'new_post.html', context)


class EditPost(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.edit_post = Post.objects.get(id=kwargs['id'])
        self.post_tags = TaggedItem.objects.filter(object_id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):

        if request.user.id == self.edit_post.user.id:

            form = PostForm(
                initial={
                    'title': self.edit_post.title,
                    'content': self.edit_post.content,
                    'user': self.edit_post.user,
                    'post_slug': self.edit_post.post_slug,
                }
            )

            tag_formset = TagFormset()
            formset = ImageFormSet()

            context = {
                'edit_post': self.edit_post,
                'post_tags': self.post_tags,
                'tag_formset': tag_formset,
                'formset': formset,
                'form': form,
                }

            return render(request, 'edit_post.html', context)

        return redirect('useraccounts:signin')

    def post(self, request, id):
        form = PostForm(request.POST, instance=self.edit_post)
        formset = ImageFormSet(request.POST, request.FILES)
        tag_formset = TagFormset(request.POST)

        if form.is_valid() and formset.is_valid() and tag_formset.is_valid():
            form.save()

            formset = formset.cleaned_data
            for image in formset:
                if image:
                    uoloaded_image = image['image']
                    post_id = self.edit_post

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
                        post_id=self.edit_post.id,
                        )

            return redirect('useraccounts:userprofile', request.user.username)

        else:
            errors = form.errors
            form = PostForm()
            tag_formset = TagFormset()
            formset = ImageFormSet()

            context = {
                'form': form,
                'errors': errors,
                'tag_formset': tag_formset,
                'formset': formset
                }

            return render(request, 'edit_post.html', context)


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

    def setup(self, request, *args, **kwargs):
        self.REACTION_FOR_ID = 8
        self.REACTION_FROM_ID = 1
        self.reaction_status = "LIKE"
        self.user = request.user.id
        self.object_id = kwargs['id']
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):

        is_liked = Reaction.objects\
            .filter(object_id=id)\
            .filter(reaction_status=self.reaction_status)\
            .filter(user=self.user)

        if is_liked.exists():
            is_liked.delete()
            return redirect(
                request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
                )

        new_reaction = Reaction(
            reaction_status=self.reaction_status,
            object_id=self.object_id,
            user=self.user,
            reaction_for_id=self.REACTION_FOR_ID,
            reaction_from_id=self.REACTION_FROM_ID,
        )
        new_reaction.save()

        return redirect(
            request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            )


class DislikePost(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.REACTION_FOR_ID = 8
        self.REACTION_FROM_ID = 1
        self.reaction_status = "DISLIKE"
        self.user = request.user.id
        self.object_id = kwargs['id']
        return super().setup(request, *args, **kwargs)

    def get(self, request, id):

        is_disliked = Reaction.objects\
            .filter(object_id=id)\
            .filter(reaction_status=self.reaction_status)\
            .filter(user=self.user)

        if is_disliked.exists():
            is_disliked.delete()
            return redirect(
                request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
                )

        new_reaction = Reaction(
            reaction_status=self.reaction_status,
            object_id=self.object_id,
            user=self.user,
            reaction_for_id=self.REACTION_FOR_ID,
            reaction_from_id=self.REACTION_FROM_ID,
        )
        new_reaction.save()

        return redirect(
            request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            )


class SinglePost(View):

    def setup(self, request, *args, **kwargs):
        self.single_post = Post.objects.filter(id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, id, post_slug):        
        reply_form = ReplyFrom(
            initial={
                    'user': request.user,
                    'post_id': list(self.single_post)[0],
                }
        )

        context = {
            "single_post": self.single_post,
            'reply_form': reply_form,
        }

        return render(request, 'singlepost.html', context)

    def post(self, request, id, post_slug):
        form = ReplyFrom(request.POST)

        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.reply_id = None
            new_reply.save()

            return redirect('posts:singlepost', id, post_slug)

        else:
            return render(request, 'posts:singlepost', id, post_slug)


class TagPosts(View):

    def get(self, request, tag_id, tag_label):

        posts_list = list(TaggedItem.objects.select_related('content_type')
                          .filter(tag_id=tag_id)
                          .filter(content_type_id=8))

        all_used_tags = TaggedItem.all_used_tags()

        context = {
            "all_used_tags": all_used_tags,
            'posts_list': posts_list,
        }

        return render(request, 'tag_posts.html', context)
