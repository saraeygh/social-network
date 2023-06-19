from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from uuid import uuid4

class User(BaseModel, AbstractUser):
    id = models.CharField(
        _("User unique ID"),
        max_length=32,
        primary_key=True,
        default=uuid4().hex
        )
    image = models.FileField(
        _("User profile picture"),
        upload_to='profile_pic/',
        )
    bio = models.CharField(
        _("A short biography of user"),
        max_length=160,
        blank=True,
        null=True,
        )