from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id = obj_id)

class Tag(models.Model):
    label = models.CharField(
        verbose_name=_("Tag label"),
        max_length=20,
        )
    
    created_at = models.DateTimeField(
        verbose_name=_("Created at:"),
        auto_now_add=True
        )
    
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at:"),
        auto_now=True
        )
    
    def used_count(self):
        return TaggedItem.objects.filter(tag=self).count()

    def __str__(self) -> str:
        return f"{self.label}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(
        Tag,
        related_name="used_tag",
        on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Post'),
        on_delete=models.CASCADE,
        )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Post ID')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    tag_from = models.ForeignKey(
        ContentType,
        verbose_name=_('User'),
        related_name="tag_from",
        on_delete=models.CASCADE
        )
    user = models.PositiveIntegerField(
        verbose_name=_('User ID')
    )
    get_user_object = GenericForeignKey('tag_from', 'user')


    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
        )
    
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
        )

    def __str__(self) -> str:
        return f"{self.tag}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']