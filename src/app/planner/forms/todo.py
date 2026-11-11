from django import forms

from app.planner.forms import PlannerFormMixin
from app.planner.models import ToDoListModel


class ToDoListCreateForm(PlannerFormMixin, forms.ModelForm):
    class Meta:
        model = ToDoListModel
        fields = ('title', 'description', 'start_date', 'end_date')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class ToDoListUpdateForm(ToDoListCreateForm):
    pass
