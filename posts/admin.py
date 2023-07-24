from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

from tags.models import TaggedItem
from reaction.models import Reaction
from .models import Post, Image, Reply, DeletedPost, DeletedReply, DeletedImage


class ImageInLine(admin.TabularInline):
    model = Image
    exclude = ['soft_delete']
    extra = 0
    verbose_name = _("Image")
    verbose_name_plural = _("Images")


class ReplyInLine(admin.TabularInline):
    autocomplete_fields = ['user', 'reply_id']
    exclude = ['soft_delete']
    model = Reply
    extra = 0
    verbose_name = _("Reply")
    verbose_name_plural = _("Replies")


class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0
    verbose_name = _("Tag")
    verbose_name_plural = _("Tags")


class ReactionInLine(GenericTabularInline):
    model = Reaction
    ct_field = "reaction_for"
    extra = 0
    verbose_name = _("Reaction")
    verbose_name_plural = _("Reactions")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReplyInLine, TagInLine, ReactionInLine]
    search_fields = ['title', 'content']
    ordering = ['title', 'created_at', 'updated_at']
    list_per_page = 10
    prepopulated_fields = {"post_slug": ("title",)}
    exclude = ['soft_delete']

    list_display = [
        'title',
        'user',
        'replies_count',
        'likes',
        'dislikes',
        'created_at',
        'updated_at'
        ]

    fieldsets = (
        (_('New post'), {
            "fields": (
                'user',
                'title',
                'content',
                'post_slug',
            ),
        }),
    )

    @admin.display(description=_("Replies count"))
    def replies_count(self, post):
        return Reply.objects.filter(post_id=post.id).count()

    @admin.display(description=_("Likes"))
    def likes(self, post):
        return Reaction.objects.filter(object_id=post.id).filter(reaction_status='LIKE').count()

    @admin.display(description=_("Dislikes"))
    def dislikes(self, post):
        return Reaction.objects.filter(object_id=post.id).filter(reaction_status='DISLIKE').count()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


@admin.register(DeletedPost)
class DeletedPostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReplyInLine, TagInLine, ReactionInLine]
    search_fields = ['title', 'content']
    ordering = ['title', 'created_at', 'updated_at']
    list_per_page = 10
    prepopulated_fields = {"post_slug": ("title",)}
    exclude = ['soft_delete']

    list_display = [
        'title',
        'user',
        'replies_count',
        'likes',
        'dislikes',
        'created_at',
        'updated_at'
        ]

    fieldsets = (
        (_('New post'), {
            "fields": (
                'user',
                'title',
                'content',
                'post_slug',
            ),
        }),
    )

    @admin.display(description=_("Replies count"))
    def replies_count(self, post):
        return Reply.objects.filter(post_id=post.id).count()

    @admin.display(description=_("Likes"))
    def likes(self, post):
        return Reaction.objects.filter(object_id=post.id).filter(reaction_status='LIKE').count()

    @admin.display(description=_("Dislikes"))
    def dislikes(self, post):
        return Reaction.objects.filter(object_id=post.id).filter(reaction_status='DISLIKE').count()

    class Meta:
        verbose_name = _("Deleted post")
        verbose_name_plural = _("Deleted posts")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    inlines = [ReplyInLine, ReactionInLine]
    search_fields = ['user', 'content']
    ordering = ['user', 'created_at', 'updated_at']
    list_per_page = 10
    exclude = ['soft_delete']

    list_display = [
        'user',
        'reply_to_post',
        'reply_to_reply',
        'content',
        'updated_at']

    fieldsets = (
        (_('New reply'), {
            "fields": (
                'user',
                'content',
                'post_id',
                'reply_id',
            ),
        }),
    )

    @admin.display(description=_("Reply to post"))
    def reply_to_post(self, reply):
        return reply.post_id

    @admin.display(description=_("Reply to reply"))
    def reply_to_reply(self, reply):
        return reply.reply_id

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")


@admin.register(DeletedReply)
class DeletedReplyAdmin(admin.ModelAdmin):
    inlines = [ReplyInLine, ReactionInLine]
    search_fields = ['user', 'content']
    ordering = ['user', 'created_at', 'updated_at']
    list_per_page = 10
    exclude = ['soft_delete']

    list_display = [
        'user',
        'reply_to_post',
        'reply_to_reply',
        'content',
        'updated_at'
        ]

    fieldsets = (
        (_('New reply'), {
            "fields": (
                'user',
                'content',
                'post_id',
                'reply_id',
            ),
        }),
    )

    @admin.display(description=_("Reply to post"))
    def reply_to_post(self, reply):
        return reply.post_id

    @admin.display(description=_("Reply to reply"))
    def reply_to_reply(self, reply):
        return reply.reply_id

    class Meta:
        verbose_name = _("Deleted reply")
        verbose_name_plural = _("Deleted replies")


@admin.register(DeletedImage)
class DeletedImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'alt_text', 'post_id', 'updated_at']
    search_fields = ['post_id', 'alt_text']
    ordering = ['created_at', 'updated_at']
    list_per_page = 10
    exclude = ['soft_delete']

    class Meta:
        verbose_name = _("Deleted image")
        verbose_name_plural = _("Deleted images")