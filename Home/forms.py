import os
import base64
from django import forms
from .models import NewsLetterSubscribers


class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': "Enter your email"}))

    class Meta:
        model = NewsLetterSubscribers
        fields = ['email',]
