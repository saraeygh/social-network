from django.db import models
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id = obj_id)

class Tag(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    label = models.CharField(
        verbose_name=_("Tag label"),
        max_length=20,
        )

    def __str__(self) -> str:
        return f"Tag Label: {self.label}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']


class TaggedItem(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"With tag {self.tag}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']