from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Category',
    )

    class Meta:
        model = Post
        fields = [
            'position',
            'name',
            'text',
            'category',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 100:
            raise ValidationError({
                "text": "Текст поста не может быть короче 100 символов."
            })

        name = cleaned_data.get("name")
        if name == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
