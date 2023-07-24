from datetime import datetime, timezone

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from reaction.models import Reaction
from tags.models import TaggedItem
from .models import UserAccount, DeletedUserAccount, Relation, DeletedRelation


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(soft_delete=False)
        
    fieldsets = (
        (_('Change username'), {
            "fields": (
                'username',
                'password',
                'user_slug',
            ),
        }),
        (_('Change user info'), {
            "fields": (
                'first_name',
                'last_name',
                'email',
                'bio',
            ),
        }),
        (_('Profile picture'), {
            "fields": (
                'image',
            ),
        }),
    )

    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'since', 'posts', 'replies', 'reactions', 'tags_used',  'following', 'follower']
    ordering = ['username', 'email']
    list_per_page = 10

    @admin.display(description=_("Joined since"))
    def since(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age

    @admin.display(description=_("Posts"))
    def posts(self, user):
        user_account_posts = user.post_set.count()
        return user_account_posts

    @admin.display(description=_("Replies"))
    def replies(self, user):
        user_account_replies = user.reply_set.count()
        return user_account_replies

    @admin.display(description=_("Reactions"))
    def reactions(self, user):
        user_account_reactions = Reaction.objects.filter(user=user.id).count()
        return user_account_reactions

    @admin.display(description=_("Tags used"))
    def tags_used(self, user):
        user_account_tags = TaggedItem.objects.filter(object_id=user.id).count()
        return user_account_tags

    @admin.display(description=_("Followings"))
    def following(self, useraccount):
        return useraccount.from_user.all().count()

    @admin.display(description=_("Followers"))
    def follower(self, useraccount):
        return useraccount.to_user.all().count()

    class Meta:
        verbose_name = _("User account")
        verbose_name_plural = _("User accounts")


@admin.register(DeletedUserAccount)
class DeletedUserAccountAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(soft_delete=True)

    fieldsets = (
        (_('Change username'), {
            "fields": (
                'username',
                'password',
                'user_slug',
            ),
        }),
        (_('Change user info'), {
            "fields": (
                'first_name',
                'last_name',
                'email',
                'bio',
            ),
        }),
        (_('Profile picture'), {
            "fields": (
                'image',
            ),
        }),
    )

    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'since', 'posts', 'replies', 'reactions', 'tags_used',  'following', 'follower']
    ordering = ['username', 'email']
    list_per_page = 10

    @admin.display(description=_("Joined since"))
    def since(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age

    @admin.display(description=_("Posts"))
    def posts(self, user):
        user_account_posts = user.post_set.count()
        return user_account_posts

    @admin.display(description=_("Replies"))
    def replies(self, user):
        user_account_replies = user.reply_set.count()
        return user_account_replies

    @admin.display(description=_("Reactions"))
    def reactions(self, user):
        user_account_reactions = Reaction.objects.filter(user=user.id).count()
        return user_account_reactions

    @admin.display(description=_("Tags used"))
    def tags_used(self, user):
        user_account_tags = TaggedItem.objects.filter(object_id=user.id).count()
        return user_account_tags

    @admin.display(description=_("Followings"))
    def following(self, useraccount):
        return useraccount.from_user.all().count()

    @admin.display(description=_("Followers"))
    def follower(self, useraccount):
        return useraccount.to_user.all().count()

    class Meta:
        verbose_name = _("Deleted user account")
        verbose_name_plural = _("Deleted user accounts")


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user', 'since']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10
    exclude = ['soft_delete']

    @admin.display(description="Joined since")
    def since(self, relation):
        relation_age = datetime.now(timezone.utc) - relation.created_at
        return relation_age

    class Meta:
        verbose_name = _("Relation")
        verbose_name_plural = _("Relations")


@admin.register(DeletedRelation)
class DeletedRelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user', 'since']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10
    exclude = ['soft_delete']

    @admin.display(description="Joined since")
    def since(self, relation):
        relation_age = datetime.now(timezone.utc) - relation.created_at
        return relation_age

    class Meta:
        verbose_name = _("Deleted relation")
        verbose_name_plural = _("Deleted relations")
