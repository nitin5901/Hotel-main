from django import forms
from .models import person
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password" )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = person
        fields = ("name" ,"phone"  )

