from django.contrib import admin
from .models import Reaction

@admin.register(Reaction)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['content_type']