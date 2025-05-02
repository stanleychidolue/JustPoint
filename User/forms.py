from typing import Required
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser


class CustomUserRegisterForm(UserCreationForm):
    # phone_no = PhoneNumberField()
    phone_no = forms.CharField(required=True, min_length=11, label="Phone")
    address = forms.Textarea()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'username', 'email', 'phone_no', "address"]


class UpdateUserInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_no', "address"]


class UpdatePasswordForm(forms.ModelForm):
    error_messages = {
        'required': 'please Fill-out this field',
        'invalid': 'fields format is not valid',
        'max_length': 'max_length is 30 chars',
        'min_length': 'password should be at least 8 Chars',
    }
    new_password1 = forms.CharField(error_messages=error_messages, min_length=8, max_length=30,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control payment-form',
                                                                      }))
    new_password2 = forms.CharField(error_messages=error_messages, min_length=8, max_length=30,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control payment-form',
                                                                      }))

    class Meta:
        model = CustomUser
        fields = ["password",]
