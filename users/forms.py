"""Forms"""
from typing import List
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """User register form"""

    email: forms.EmailField = forms.EmailField(required=True)

    class Meta:
        model :type= User
        fields: List[str] = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """User update form"""

    email: forms.EmailField = forms.EmailField()
    first_name: forms.CharField = forms.CharField(max_length=30)
    last_name: forms.CharField = forms.CharField(max_length=30)

    class Meta:
        model : type= User
        fields: List[str] = ["username", "email", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    """User profile update form"""

    class Meta:
        model :type = Profile
        fields: List[str] = ["image"]
