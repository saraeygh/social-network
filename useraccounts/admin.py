from django.contrib import admin
from .models import UserAccount, Relation
from datetime import datetime, timezone

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name', ]
    list_display = ['username', 'email', 'first_name', 'last_name', 'since_created', 'updated_at']
    list_editable = []
    ordering = ['username', 'email', 'created_at', 'updated_at']
    list_per_page = 10

    def since_created(self, user):
        user_account_age = datetime.now(timezone.utc) - user.created_at
        return user_account_age


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user']
    search_fields = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
    list_per_page = 10