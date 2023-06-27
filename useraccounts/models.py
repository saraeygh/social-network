from django.db import models
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class UserAccount(BaseModel, AbstractUser, CreateTimeMixin, UpdateTimeMixin):

    # Model fields
    objects = UserManager()
    
    image = models.FileField(
        verbose_name = _("User profile picture"),
        upload_to = 'profilepics/',
        blank=True,
        null=True,
        )
    bio = models.CharField(
        verbose_name = _("User short biography"),
        max_length = 160,
        blank = True,
        null = True,
        )
    
    user_slug = models.SlugField(
        verbose_name=_("User slug"),
        unique=True,
        default = 'username',
        )
    
    def save(self, *args, **kwargs):
        self.user_slug = self.username
        super(UserAccount, self).save(*args, **kwargs)

    # Model methods
    def following(self):
        return self.from_user.all().count()
    
    def follower(self):
        return self.to_user.all().count()

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        ordering = ['-created_at', '-updated_at']
    

class Relation(BaseModel, CreateTimeMixin):
    from_user = models.ForeignKey(
        UserAccount,
        verbose_name = _("from_user"),
        on_delete=models.CASCADE,
        related_name='from_user'
        )
    to_user = models.ForeignKey(
        UserAccount,
        verbose_name = _("to_user"),
        on_delete=models.CASCADE,
        related_name='to_user'
        )
    
    def __str__(self) -> str:
        return f" {self.from_user} follows {self.to_user}"
    
    class Meta:
        ordering = ['-created_at']
    