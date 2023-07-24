from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreateTimeMixin, UpdateTimeMixin
from useraccounts.models import UserAccount
from reaction.models import Reaction
from tags.models import TaggedItem


class NotSoftDeleted(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=False)


class SoftDeleted(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=True)


class Post(BaseModel, CreateTimeMixin, UpdateTimeMixin):

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
        )

    def tags(self):
        return TaggedItem.objects.filter(object_id=self.id)

    def replies(self):
        return Reply.objects.filter(post_id=self.id).filter(reply_id_id=None)

    def nested_replies(self):
        return Reply.objects.filter(post_id=self.id).filter(~Q(reply_id_id=None))

    def images(self):
        return Image.objects.filter(post_id=self.id)

    def replies_count(self):
        return Reply.objects.filter(post_id=self.id).count()

    def likes(self):
        return Reaction.objects.filter(object_id=self.id).filter(reaction_status='LIKE').count()

    def dislikes(self):
        return Reaction.objects.filter(object_id=self.id).filter(reaction_status='DISLIKE').count()

    def delete_post(self):
        self.delete()
        post_taggeditem = TaggedItem.objects.filter(content_type_id=8).filter(object_id=self.id)
        if post_taggeditem:
            for item in post_taggeditem:
                item.delete()
        return None

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class DeletedPost(Post):
    objects = SoftDeleted()

    class Meta:
        proxy = True
        verbose_name = _("Deleted post")
        verbose_name_plural = _("Deleted posts")


class Image(BaseModel, CreateTimeMixin, UpdateTimeMixin):
    image = models.FileField(
        upload_to='postpic/',
        max_length=100,
        verbose_name=_("Image")
        )

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
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class DeletedImage(Image):
    objects = SoftDeleted()

    class Meta:
        proxy = True
        verbose_name = _("Deleted image")
        verbose_name_plural = _("Deleted images")


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
        verbose_name=_("Post ID")
        )
    reply_id = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Reply ID")
        )

    def __str__(self) -> str:
        return f"{self.content}"

    class Meta:
        ordering = ['-created_at', '-updated_at']
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")


class DeletedReply(Reply):
    objects = SoftDeleted()

    class Meta:
        proxy = True
        verbose_name = _("Deleted reply")
        verbose_name_plural = _("Deleted replies")
