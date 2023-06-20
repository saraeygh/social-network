from django.contrib import admin
from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['get_content_object', 'reaction_status', 'user']
    list_editable = ['reaction_status']
    list_per_page = 10