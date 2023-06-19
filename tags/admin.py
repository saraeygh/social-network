from django.contrib import admin
from .models import Tag, TaggedItem



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label']
    ordering = ['label']
    list_per_page = 10

    #def used_count(self, tag):
    #    tag.objects.filter(count=Count('tag_id'))
    #    pass


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tag']
    list_display = ['content_type']