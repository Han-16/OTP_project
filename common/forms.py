from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    position = forms.CharField(max_length = 200)
    symmetric_key = forms.CharField(max_length=128, required=False)
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "position",'symmetric_key')



