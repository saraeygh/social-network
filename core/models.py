from django.db import models
from uuid import uuid4
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    unique_id = models.CharField(
        max_length = 32,
        primary_key = True,
        default = uuid4().hex
        )
    class Meta:
        abstract = True


class CreateTimeMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created at:"),
        auto_now_add=True
        )
    class Meta:
        abstract = True
    

class UpdateTimeMixin(models.Model):
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at:"),
        auto_now=True
        )
    class Meta:
        abstract = True