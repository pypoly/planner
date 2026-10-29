from django import forms

from app.planner.models import ToDoListModel


class ToDoUpdateForm(forms.ModelForm):
    class Meta:
        model = ToDoListModel
        fields = '__all__'
