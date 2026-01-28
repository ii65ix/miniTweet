from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "اكتب تغريدة جديدة...",
                }
            )
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="اختياري")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
