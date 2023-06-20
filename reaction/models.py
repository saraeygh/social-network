from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Reaction(models.Model):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'

    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    status = models.CharField(max_length=50, choices=REACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    reaction_from = models.ForeignKey(
        ContentType,
        related_name="reaction_from",
        on_delete=models.CASCADE
        )
    user = models.PositiveIntegerField()
    get_user_object = GenericForeignKey()

    created_at = models.DateTimeField(
        verbose_name=_("Created at:"),
        auto_now_add=True
        )
    
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at:"),
        auto_now=True
        )
    
    
    def __str__(self) -> str:
        return f"Reaction: {self.status}"