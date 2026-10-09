from django import forms

from app.planner.models import TaskModel, ToDoListModel


class DetailTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')

class CreateTaskForm(forms.ModelForm):
    tasklist = forms.ModelChoiceField(queryset=ToDoListModel.objects.filter(archived=False), widget=forms.HiddenInput())
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status', 'tasklist')

class DeleteTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status')
