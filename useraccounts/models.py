from uuid import uuid4

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin


class NotSoftDeleted(UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(soft_delete=False)


class SoftDeleted(UserManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(soft_delete=True)


class UserAccount(BaseModel, AbstractUser, CreateTimeMixin, UpdateTimeMixin):

    objects = NotSoftDeleted()
    objects_all = UserManager()

    image = models.FileField(
        verbose_name=_("Profile picture"),
        upload_to='profilepics/',
        blank=True,
        null=True,
        )
    bio = models.CharField(
        verbose_name=_("Bio"),
        max_length=160,
        blank=True,
        null=True,
        )

    user_slug = models.SlugField(
        verbose_name=_("User slug"),
        default=uuid4().hex,
        )

    def save(self, *args, **kwargs):
        self.user_slug = self.username
        super(UserAccount, self).save(*args, **kwargs)

    def following(self):
        return self.from_user.all().count()

    def follower(self):
        return self.to_user.all().count()

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        ordering = ['-created_at', '-updated_at']


class DeletedUserAccount(UserAccount):
    objects = SoftDeleted()

    class Meta:
        proxy = True


class Relation(BaseModel, CreateTimeMixin):
    from_user = models.ForeignKey(
        UserAccount,
        verbose_name=_("from_user"),
        on_delete=models.CASCADE,
        related_name='from_user'
        )

    to_user = models.ForeignKey(
        UserAccount,
        verbose_name=_("to_user"),
        on_delete=models.CASCADE,
        related_name='to_user'
        )

    def __str__(self) -> str:
        return f" {self.from_user} follows {self.to_user}"

    class Meta:
        ordering = ['-created_at']


class DeletedRelation(Relation):
    objects = SoftDeleted()

    class Meta:
        proxy = True
