from django import forms


class PlannerFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'nb-input form-select'
            else:
                widget.attrs['class'] = 'nb-input'
            if isinstance(field, forms.DateField) and (
                widget.attrs.get('type') == 'date'
                or getattr(widget, 'input_type', None) == 'date'
            ):
                widget.attrs['type'] = 'date'
                widget.format = '%Y-%m-%d'
                field.input_formats = ['%Y-%m-%d']
