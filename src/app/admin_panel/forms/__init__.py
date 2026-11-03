from django import forms


class BootstrapFormMixin:
    """Add Bootstrap classes to widgets so templates can render plain markup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault('class', 'form-select')
            elif isinstance(widget, forms.FileInput):
                widget.attrs.setdefault('class', 'form-control')
            else:
                widget.attrs.setdefault('class', 'form-control')

            if isinstance(field, forms.DateField) and widget.attrs.get('type') == 'date':
                field.input_formats = ['%Y-%m-%d']
