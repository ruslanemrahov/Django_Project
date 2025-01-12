# forms.py
from django import forms
from .models import Post, Comment
from django_recaptcha.fields import ReCaptchaField

class PostForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]
class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Comment
        fields = [
            'name',
            'content',
        ]