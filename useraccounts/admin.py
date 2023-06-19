from django.contrib import admin
from .models import UserAccount, Relation

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['username']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user']