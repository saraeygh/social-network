from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['get_content_object', 'reaction_status', 'by_user']
    list_editable = ['reaction_status']
    list_per_page = 10

    @admin.display(description=_("By"))
    def by_user(self, reaction):
        return reaction.get_user_object

    class Meta:
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")