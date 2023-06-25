from django.db import models
from django.db.models import QuerySet
from django.db.models.query import QuerySet
from django.contrib.auth.models import BaseUserManager

from django.utils.translation import gettext_lazy as _


class AppManager(BaseUserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(soft_delete=False)
    
    def archived(self) -> QuerySet:
        return super().get_queryset().filter(soft_delete=True)

class BaseModel(models.Model, models.Manager):

    objects = AppManager()

    class Meta:
        abstract = True

    soft_delete = models.BooleanField(default = False)
    # objects = AppManager()

    
    def delete(self):
        """
        Mark record as soft deleted
        """
        self.soft_delete = True
        self.save()


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