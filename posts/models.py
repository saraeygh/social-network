from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from useraccounts.models import UserAccount
from reaction.models import Reaction


class Post(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    
    # Model Fields
    title = models.CharField(
        verbose_name=_("Post title"),
        max_length=255
        )
    
    content = models.TextField(verbose_name=_("Post content"))

    user = models.ForeignKey(
        UserAccount,
        verbose_name=_("User"),
        on_delete=models.CASCADE
        )

    post_slug = models.SlugField(
        verbose_name=_("post slug"),
        unique=True,
        )

    def replies_count(self):
        return Reply.objects.filter(post_id=self.id).count()

    def likes(self):
        return Reaction.objects.filter(object_id=self.id).filter(reaction_status='LIKE').count()

    def dislikes(self):
        return Reaction.objects.filter(object_id=self.id).filter(reaction_status='DISLIKE').count()

    def __str__(self) -> str:
        return f"{self.title}"


    class Meta:
        ordering = ['-created_at', '-updated_at']


class Image(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    image = models.FileField(
        verbose_name=_("Post image(s)"),
        upload_to='postpic/',
        max_length=100)
    alt_text = models.TextField(verbose_name=_("Image alt"))
    post_id = models.ForeignKey(
        Post,
        verbose_name=_("Post"),
        on_delete=models.CASCADE,
        )
    
    
    def __str__(self) -> str:
        return f"ALT: {self.alt_text}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']
    

class Reply(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    content = models.TextField(verbose_name=_("Reply text"))
    
    user = models.ForeignKey(
        UserAccount,
        verbose_name=_("User"),
        on_delete=models.CASCADE
        )
    
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        )
    reply_id = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        )
    
    def __str__(self) -> str:
        return f"Reply to: {self.post_id}"
    
    class Meta:
        ordering = ['-created_at', '-updated_at']