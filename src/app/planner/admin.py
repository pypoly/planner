from django.contrib import admin

from app.planner.models import TaskModel, ToDoListModel

# @admin.register(TaskModel)
# class TaskAdmin(admin.ModelAdmin):
#     fields = ['name']
#     list_display = ['name', 'status']
#     list_editable = ['status']


class TaskInline(admin.StackedInline):
    model = TaskModel
    extra = 0


@admin.register(ToDoListModel)
class ToDolistAdmin(admin.ModelAdmin):
    fields = ['title', 'user',]
    list_display = ['title', 'user', 'progress', 'archived']
    list_editable = ['progress','archived']
    inlines = (TaskInline,)

