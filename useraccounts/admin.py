from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, Relation
from datetime import datetime, timezone

@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'image',
        'bio',
    )
    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'first_name', 'last_name', 'since_created', 'following', 'follower']
    list_editable = []
    ordering = ['username', 'email', 'created_at', 'updated_at']
    list_per_page = 10

    def since_created(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age
    
    def following(self, useraccount):
        return useraccount.from_user.all().count()
    
    def follower(self, useraccount):
        return useraccount.to_user.all().count()


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10