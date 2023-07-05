from django import forms
from django.forms import inlineformset_factory
from .models import Post, Image


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
            
        widgets = {
            'user': forms.HiddenInput(),
            'post_slug': forms.HiddenInput(),
            'soft_delete': forms.HiddenInput(),
        }


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = "__all__"


ImageFormSet = inlineformset_factory(
    Post, Image, form=ImageForm,
    extra=1, can_delete=True, can_delete_extra=True
)