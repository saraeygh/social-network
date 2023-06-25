from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Post, Image, Reply
from tags.models import TaggedItem
from reaction.models import Reaction

class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0

class ReplyInLine(admin.TabularInline):
    model = Reply
    extra = 0


class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0

class ReactionInLine(GenericTabularInline):
    model = Reaction
    ct_field = "reaction_for"
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   inlines = [ImageInLine, ReplyInLine, TagInLine, ReactionInLine]
   list_display = ['title', 'user', 'replies_count', 'created_at', 'updated_at']
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