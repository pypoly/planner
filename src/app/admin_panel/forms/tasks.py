from django import forms

from app.planner.models import TaskModel


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'