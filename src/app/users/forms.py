from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User


class PlannerWidgetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.input_type in ('hidden', 'checkbox'):
                continue
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{classes} nb-input'.strip()


class UserRegisterForm(PlannerWidgetMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(PlannerWidgetMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class MyPasswordChangeForm(PlannerWidgetMixin, PasswordChangeForm):
    pass


class PlannerAuthenticationForm(PlannerWidgetMixin, AuthenticationForm):
    pass
