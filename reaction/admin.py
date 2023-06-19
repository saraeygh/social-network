from django.contrib import admin
from .models import Reaction

@admin.register(Reaction)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'status']
    list_editable = ['status']
    ordering = ['content_type', 'object_id']
    list_per_page = 10