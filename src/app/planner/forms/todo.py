from django import forms
from django.contrib.auth.models import User

from app.planner.models import ToDoListModel


class ToDoListCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = ToDoListModel
        fields = ('user', 'title', 'description')


class ToDoListUpdateForm(forms.ModelForm):
     class Meta:
         model = ToDoListModel
         fields = ('title', 'description')
