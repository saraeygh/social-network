from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)


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
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedItem(models.Model):
    objects = TaggedItemManager()

    tag = models.ForeignKey(
        Tag,
        related_name="used_tag",
        on_delete=models.CASCADE,
        verbose_name=_("Tag")
        )

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        on_delete=models.CASCADE,
        )
    object_id = models.PositiveIntegerField(
        verbose_name=_('ID')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    tag_from = models.ForeignKey(
        ContentType,
        verbose_name=_('Content type'),
        related_name="tag_from",
        on_delete=models.CASCADE
        )
    user = models.PositiveIntegerField(
        verbose_name=_('ID')
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

    def add_tagged_item(self, tag, user_id, post_id):
        new_tagged_item = TaggedItem.objects.create(
            tag=tag,
            object_id=post_id,
            user=user_id,
            content_type_id=8,
            tag_from_id=1,
        )
        new_tagged_item.save()

    @staticmethod
    def all_used_tags():
        all_tags = []
        all_tagged_items = TaggedItem.objects.all()
        for tagged_item in all_tagged_items:
            if tagged_item.tag in all_tags:
                continue
            all_tags.append(tagged_item.tag)
        return all_tags

    def __str__(self) -> str:
        return f"{self.tag}"

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = _("Tagged item")
        verbose_name_plural = _("Tagged items")
