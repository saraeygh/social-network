from django.contrib import admin
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline
from useraccounts.models import UserAccount
from .models import Post, Image, Reply
from tags.models import TaggedItem, Tag
from reaction.models import Reaction


class ImageInLine(admin.TabularInline):
    model = Image
    exclude = ['soft_delete']
    extra = 0


class ReplyInLine(admin.TabularInline):
    autocomplete_fields = ['user', 'reply_id']
    exclude = ['soft_delete']
    model = Reply
    extra = 0


class TagInLine(GenericTabularInline):

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "tag_from":
            kwargs["queryset"] = ContentType.objects.filter(id=1)            
        return super(TagInLine, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0


class ReactionInLine(GenericTabularInline):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "reaction_from":
            kwargs["queryset"] = ContentType.objects.filter(id=1)            
        return super(ReactionInLine, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    model = Reaction
    ct_field = "reaction_for"
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReplyInLine, TagInLine, ReactionInLine]
    list_display = ['title', 'user', 'replies_count', 'likes', 'dislike', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['title', 'created_at', 'updated_at']
    list_per_page = 10
    prepopulated_fields = {
        "post_slug": ("title",)
        }
    fieldsets = (
        ('New post', {
            "fields": (
                'user',
                'title',
                'content',
                'post_slug',
            ),
        }),
    )
    exclude = ['soft_delete']

    def replies_count(self, post):
        return Reply.objects.filter(post_id=post.id).count()
   
    def likes(self, post):
        return Reaction.objects.filter(id=post.id).filter(reaction_status='LIKE').count()
   
    def dislike(self, post):
        return Reaction.objects.filter(id=post.id).filter(reaction_status='DISLIKE').count()


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    inlines = [ReplyInLine, ReactionInLine]
    list_display = ['user', 'reply_to', 'created_at', 'updated_at']
    search_fields = ['user', 'content']
    ordering = ['user', 'created_at', 'updated_at']
    list_per_page = 10
    exclude = ['soft_delete']

    fieldsets = (
        ('New reply', {
            "fields": (
                'user',
                'content',
                'post_id',
                'reply_id',
            ),
        }),
    )

    def reply_to(self, reply):
        return reply.post_id