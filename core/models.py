from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


# Custome managers
class AppManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=False)

    def archived(self):
        return super().get_queryset().filter(soft_delete=True)


# Base model instead of Django default model
class BaseModel(models.Model, models.Manager):

    objects = AppManager()
    soft_delete = models.BooleanField(
        default=False,
        verbose_name=_("Soft delete")
        )

    def delete(self):
        self.soft_delete = True
        self.save()

    class Meta:
        abstract = True


class CreateTimeMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
        )

    class Meta:
        abstract = True


class UpdateTimeMixin(models.Model):
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
        )

    class Meta:
        abstract = True
