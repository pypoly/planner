from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from app.planner.models import ToDoListModel, TaskModel


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin_panel/index.html'


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'admin_panel/user_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        ctx['todos'] = ToDoListModel.objects.filter(user=user_pk)
        return ctx

class UserTasksView(DetailView):
    model = ToDoListModel
    context_object_name = 'todo'
    template_name = 'admin_panel/user_tasks.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        todo_list_pk = self.kwargs['pk']
        ctx['tasks'] = TaskModel.objects.filter(tasklist_id=todo_list_pk)
        return ctx

class StatisticUserView(TemplateView):
    template_name = 'admin_panel/statistic.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_count = User.objects.count()
        ctx['user_count'] = user_count
        todo_count = ToDoListModel.objects.count()
        ctx['todo_count'] = todo_count
        return ctx



