from django.db import models
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _


class UserAccount(BaseModel, AbstractUser, CreateTimeMixin, UpdateTimeMixin):
    image = models.FileField(
        verbose_name = _("User profile picture"),
        upload_to = 'profilepic/',
        blank=True,
        null=True,
        )
    bio = models.CharField(
        verbose_name = _("User short biography"),
        max_length = 160,
        blank = True,
        null = True,
        )
    
    
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
    