from django.urls import reverse
from django.views.generic import DetailView, CreateView, DeleteView

from app.planer.forms.todo import ToDoListCreateForm
from app.planer.models import ToDoListModel


class ToDoDetailView(DetailView):
    model = ToDoListModel
    # form_class = TaskDetailForm
    template_name = 'planer/todo/todolist_detail.html'


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


