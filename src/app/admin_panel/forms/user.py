from django import forms
from django.contrib.auth.models import User


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name',)
#


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name')


class UserPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)

