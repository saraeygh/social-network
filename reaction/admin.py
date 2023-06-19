from django.contrib import admin
from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'status']
    list_editable = ['status']
    list_per_page = 10