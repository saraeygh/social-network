from django.db import models
from django.db.models import Manager, QuerySet
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


# class AppManager(Manager):
#     """
#     To exclude all soft deleted records
#     """
#     def get_queryset(self):
#         return QuerySet(self.model, using=self._db).exclude(soft_delete=True)


class BaseModel(models.Model):
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