from django.shortcuts import redirect
from django.urls import reverse
from django.utils import archive
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from app.planer.forms.todo import ToDoListCreateForm, ToDoListUpdateForm
from app.planer.models import ToDoListModel, TaskStatus


class ToDoDetailView(DetailView):
    model = ToDoListModel
    # form_class = TaskDetailForm
    template_name = 'planer/todo/todolist_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        ctx['tasks'] = obj.tasks.only('name').order_by('start_date','pk')
        return ctx


class CreateToDoListView(CreateView):
    model = ToDoListModel
    form_class = ToDoListCreateForm
    template_name = 'planer/todo/todolist_create_form.html'

    def get_initial(self):
        return {
            'user': self.request.user,
        }
    
    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class TodoListDeleteView(DeleteView):
    model = ToDoListModel
    template_name = 'planer/todo/todolist_delete.html'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.archived = True
        obj.save()
        return redirect(reverse('index'))

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class ToDoListUpdateView(UpdateView):
    model = ToDoListModel
    form_class = ToDoListUpdateForm
    template_name = 'planer/todo/todolist_update_form.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})

