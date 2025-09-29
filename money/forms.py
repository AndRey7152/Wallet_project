from django import forms

from .models import User

class CreateUser(forms.ModelForm):
    class Meta:
        model = User
        field = ['user_name', 'email']