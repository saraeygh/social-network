from django.contrib import admin
from .models import Tag, TaggedItem



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label', 'used_count']
    ordering = ['label']
    list_per_page = 10

    def used_count(self, tag):
        return Tag.objects.filter(label = tag.label).count()      


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tag']
    list_display = ['tagged_item', 'tag']
    
    def tagged_item(self, taggeditem):
        return taggeditem.content_object