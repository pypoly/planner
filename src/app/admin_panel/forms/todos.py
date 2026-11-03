from django import forms

from app.admin_panel.forms import BootstrapFormMixin
from app.planner.models import ToDoListModel


class ToDoUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ToDoListModel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
