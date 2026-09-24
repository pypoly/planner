from django import forms
from django.contrib.auth.models import User

from app.planer.models import ToDoListModel, TaskModel


class ToDoListCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = ToDoListModel
        fields = ('user', 'title', 'description')

class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')

class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')