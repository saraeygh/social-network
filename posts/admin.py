from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Post, Image, Reply
from tags.models import TaggedItem
from reaction.models import Reaction

class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0

class ReplyInLine(admin.TabularInline):
    model = Reply
    extra = 0


class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 0

class ReactionInLine(GenericTabularInline):
    model = Reaction
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReplyInLine, TagInLine, ReactionInLine]
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    ordering = ['title', 'created_at', 'updated_at']
    list_per_page = 10