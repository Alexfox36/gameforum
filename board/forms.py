from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_title',
            'post_content',
            'post_category',

        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("post_title")

        if description is not None and len(description) < 10:
            raise ValidationError({
                "description": "Описание не может быть менее 10 символов."
            })

        name = cleaned_data.get("post_content")
        if name is None:
            raise ValidationError(
                "Описание не может быть пустым."
            )

        return cleaned_data
