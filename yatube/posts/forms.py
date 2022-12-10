from django import forms
from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        labels = {'group': 'Группа', 'text': 'Сообщение'}
        help_texts = {'group': 'Выберите группу', 'text': 'Введите ссообщение'}
        fields = ['group', 'text', 'image']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control',}),
            'group': forms.Select(attrs={'class': 'form-control',}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
