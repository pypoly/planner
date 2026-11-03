from django import forms
from django.contrib.auth.models import User

from app.admin_panel.forms import BootstrapFormMixin


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name')


class UserPasswordForm(BootstrapFormMixin, forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)

