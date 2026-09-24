from django import forms

from app.planer.models import TaskModel


class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')
