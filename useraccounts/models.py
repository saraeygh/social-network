from django.db import models
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class UserAccount(BaseModel, User, CreateTimeMixin, UpdateTimeMixin):
    image = models.FileField(
        verbose_name = _("User profile picture"),
        upload_to = 'profile_pic/',
        )
    bio = models.CharField(
        verbose_name = _("User short biography"),
        max_length = 160,
        blank = True,
        null = True,
        )
    

class Relation(BaseModel, CreateTimeMixin):
    from_user = models.ForeignKey(
        UserAccount,
        verbose_name = _("Following"),
        on_delete=models.CASCADE,
        related_name='following'
        )
    to_user = models.ForeignKey(
        UserAccount,
        verbose_name = _("Follower"),
        on_delete=models.CASCADE,
        related_name='follower'
        )
    