from django.contrib import admin
from .models import Post, Image

class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]
    list_display = ['title', 'created_at', 'updated_at']


