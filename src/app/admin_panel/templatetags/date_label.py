from django import template

from app.planner.models import TaskStatus

register = template.Library()


@register.filter
def date_label(value):
    if value:
        return value
    else:
        return '---'



