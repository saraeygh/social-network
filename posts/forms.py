from django import forms
from django.forms import inlineformset_factory, formset_factory
from .models import Post, Reply, Image
from tags.models import Tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"
            
        widgets = {
            'user': forms.HiddenInput(),
            'post_slug': forms.HiddenInput(),
            'soft_delete': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ReplyFrom(forms.ModelForm):

    class Meta:
        model = Reply
        fields = "__all__"
        exclude = [
            'soft_delete',
        ]

        widgets = {
            'user': forms.HiddenInput(),
            'post_id': forms.HiddenInput(),
            'reply_id': forms.HiddenInput(),
        }


class TagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tag
        fields = "__all__"
        extras = {
            'label': 3,
        }


TagFormset = formset_factory(
    TagForm,
    extra=3
)


class ImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Image
        fields = [
            'image',
        ]


ImageFormSet = inlineformset_factory(
    Post,
    Image,
    form=ImageForm,
    extra=3,
    can_delete=True,
)