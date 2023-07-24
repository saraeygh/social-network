from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class ReactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class Reaction(models.Model):

    objects = ReactionManager()

    LIKE = _('LIKE')
    DISLIKE = _('DISLIKE')

    REACTION_CHOICES = [
        (LIKE, _('Like')),
        (DISLIKE, _('Dislike')),
    ]

    reaction_status = models.CharField(
        max_length=50,
        choices=REACTION_CHOICES,
        verbose_name=_("Reaction status")
        )
    reaction_for = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content type")
        )
    object_id = models.PositiveIntegerField(verbose_name=_("ID"))
    get_content_object = GenericForeignKey('reaction_for', 'object_id')

    reaction_from = models.ForeignKey(
        ContentType,
        related_name="reaction_from",
        on_delete=models.CASCADE,
        verbose_name=_("Content type")
        )
    user = models.PositiveIntegerField(verbose_name=_("ID"))
    get_user_object = GenericForeignKey('reaction_from', 'user')

    created_at = models.DateTimeField(
        verbose_name=_("Created at:"),
        auto_now_add=True
        )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at:"),
        auto_now=True
        )

    def __str__(self) -> str:
        return f"{self.reaction_status}"