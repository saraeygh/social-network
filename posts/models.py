from django.db import models
from django.utils.translation import gettext as _
from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin

class Post(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    title = models.CharField(
        verbose_name = _("Post title"),
        max_length=255
        )
    
    content = models.TextField(verbose_name = _("Post content"))


class Image(BaseModel):
    image = models.FileField(
        verbose_name = _("Post image(s)"),
        upload_to='postpic/',
        max_length=100)
    alt_text = models.TextField(verbose_name = _("Image alt"))
    post_id = models.ForeignKey(
        Post,
        verbose_name=_("Image for post"),
        on_delete=models.CASCADE
        )