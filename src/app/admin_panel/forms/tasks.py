from django import forms

from app.admin_panel.forms import BootstrapFormMixin
from app.planner.models import TaskModel


class TaskUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'start_date', 'end_date', 'order', 'status', 'deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
