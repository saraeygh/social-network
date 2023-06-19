from django.contrib import admin
from .models import UserAccount, Relation

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']