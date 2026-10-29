from django.contrib.auth.models import User
from django.views.generic import UpdateView, DetailView
from django.views.generic.list import ListView

from app.admin_panel.forms.todos import ToDoUpdateForm
from app.planner.models import ToDoListModel, TaskModel



class ToDoListView(ListView):
    model = ToDoListModel
    context_object_name = 'todo_list'
    template_name = 'admin_panel/todo-list.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     user_pk = self.kwargs['pk']
    #     ctx['todos'] = ToDoListModel.objects.filter(user=user_pk)
    #     return ctx

class ToDoDetailView(DetailView):
    model = ToDoListModel
    context_object_name = 'todo'
    template_name = 'admin_panel/todo-detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        todo_list_pk = self.kwargs['pk']
        ctx['tasks'] = TaskModel.objects.filter(tasklist_id=todo_list_pk).order_by('order', 'created_at')
        return ctx

class ToDoUpdateView(UpdateView):
    model = ToDoListModel
    form_class = ToDoUpdateForm
    context_object_name = 'todo'
    template_name = 'admin_panel/todo-update.html'

# class AdminToDoUpdateView(UpdateView):
#     model = ToDoListModel
#     context_object_name = 'todo_list'
    # template_name = ''
