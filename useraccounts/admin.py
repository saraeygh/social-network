from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, DeletedUserAccount, Relation, DeletedRelation
from reaction.models import Reaction
from tags.models import TaggedItem
from datetime import datetime, timezone

@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(soft_delete=False)
        
    fieldsets = (
        ('Change username', {
            "fields": (
                'username',
                'password',
                'user_slug',
            ),
        }),
        ('Change user info', {
            "fields": (
                'first_name',
                'last_name',
                'email',
                'bio',
            ),
        }),
        ('Profile picture', {
            "fields": (
                'image',
            ),
        }),
    )
    
    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'since', 'posts', 'replies', 'reactions', 'tags_used',  'following', 'follower']
    ordering = ['username', 'email']
    list_per_page = 10

    
    def since(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age
    
    def posts(self, user):
        user_account_posts = user.post_set.count()
        return user_account_posts
    
    def replies(self, user):
        user_account_replies = user.reply_set.count()
        return user_account_replies
    
    def reactions(self, user):
        user_account_reactions = Reaction.objects.filter(user=user.id).count()
        return user_account_reactions
    
    def tags_used(self, user):
        user_account_tags = TaggedItem.objects.filter(object_id=user.id).count()
        return user_account_tags
    
    def following(self, useraccount):
        return useraccount.from_user.all().count()
    
    def follower(self, useraccount):
        return useraccount.to_user.all().count()


@admin.register(DeletedUserAccount)
class DeletedUserAccountAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(soft_delete=True)
        
    fieldsets = (
        ('Change username', {
            "fields": (
                'username',
                'password',
            ),
        }),
        ('Change user info', {
            "fields": (
                'first_name',
                'last_name',
                'email',
                'bio',
            ),
        }),
        ('Profile picture', {
            "fields": (
                'image',
            ),
        }),
    )
    
    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'since', 'posts', 'replies', 'reactions', 'tags_used',  'following', 'follower']
    ordering = ['username', 'email']
    list_per_page = 10

    
    def since(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age
    
    def posts(self, user):
        user_account_posts = user.post_set.count()
        return user_account_posts
    
    def replies(self, user):
        user_account_replies = user.reply_set.count()
        return user_account_replies
    
    def reactions(self, user):
        user_account_reactions = Reaction.objects.filter(user=user.id).count()
        return user_account_reactions
    
    def tags_used(self, user):
        user_account_tags = TaggedItem.objects.filter(object_id=user.id).count()
        return user_account_tags
    
    def following(self, useraccount):
        return useraccount.from_user.all().count()
    
    def follower(self, useraccount):
        return useraccount.to_user.all().count()
    

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user', 'since']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10
    exclude = ['soft_delete']

    def since(self, relation):
        relation_age = datetime.now(timezone.utc) - relation.created_at
        return relation_age
    

@admin.register(DeletedRelation)
class DeletedRelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user', 'since']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10
    exclude = ['soft_delete']

    def since(self, relation):
        relation_age = datetime.now(timezone.utc) - relation.created_at
        return relation_age