from django.contrib import admin
from .models import Post, Image, Reply

class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0

class ReplyInLine(admin.TabularInline):
    model = Reply
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReplyInLine]
    list_display = ['title', 'created_at', 'updated_at']