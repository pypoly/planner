from django import template

from app.planer.models import TaskStatus

register = template.Library()


@register.filter
def status_label(value):
    return {
        TaskStatus.PENDING: '😀 Ждемс',
        TaskStatus.DONE: "👻 Готово",
        TaskStatus.CANCELED: "☹️ Отмена"
    }.get(value, 'Неизвестно')

