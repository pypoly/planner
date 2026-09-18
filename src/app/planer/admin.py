from django.contrib import admin

from app.planer.models import Task, Tasklist

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']

@admin.register(Tasklist)
class TasklistAdmin(admin.ModelAdmin):
    fields = ['title']
    list_display = ['title']
