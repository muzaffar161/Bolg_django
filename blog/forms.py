from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from dj_turnstile.fields import TurnstileField

from .models import Article, AuthorProfile, Comment


class ArticleForm(forms.ModelForm):
    turnstile = TurnstileField()

    class Meta:
        model = Article
        fields = [
            "title",
            "category",
            "tags",
            "excerpt",
            "body",
            "image",
            "status",
            "is_featured",
        ]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 12}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    turnstile = TurnstileField()

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Share your thoughts about this story...",
                }
            ),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    turnstile = TurnstileField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginWithTurnstileForm(AuthenticationForm):
    turnstile = TurnstileField()


class AuthorProfileForm(forms.ModelForm):
    turnstile = TurnstileField()

    class Meta:
        model = AuthorProfile
        fields = ["bio", "avatar", "website"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
