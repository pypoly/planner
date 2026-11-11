from django import forms

from app.planner.forms import PlannerFormMixin
from app.planner.models import TaskModel


class CreateTaskForm(PlannerFormMixin, forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status', 'start_date', 'end_date', 'deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class UpdateTaskForm(CreateTaskForm):
    pass
