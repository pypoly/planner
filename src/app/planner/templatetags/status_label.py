from django import template

from app.planner.models import TaskStatus

register = template.Library()


@register.filter
def status_label(value):
    return {
        TaskStatus.PENDING: '⏳ Ожидает',
        TaskStatus.DONE: "✅ Готово",
        TaskStatus.CANCELED: "❌ Отмена"
    }.get(value, '❔ Неизвестно')

