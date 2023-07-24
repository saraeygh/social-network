from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
    list_display = ['label', 'used_count', 'created_at']
    ordering = ['label']
    list_per_page = 10

    @admin.display(description=_("Used count"))
    def used_count(self, tag):
        return TaggedItem.objects.filter(tag=tag).count()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tag']
    list_display = ['tagged_item', 'tag', 'by_user', 'updated_at']

    @admin.display(description=_("Content type"))
    def tagged_item(self, taggeditem):
        return taggeditem.content_object

    @admin.display(description=_("By"))
    def by_user(self, taggeditem):
        return taggeditem.get_user_object

    class Meta:
        verbose_name = _("Tagged item")
        verbose_name_plural = _("Tagged item")