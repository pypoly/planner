from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from app.planer.forms import ToDoListCreateForm, TaskDetailForm
from app.planer.models import TaskModel, ToDoListModel


# Tasks
class IndexView(ListView):
    model = ToDoListModel
    template_name ='planer/index.html'
    context_object_name = 'todolists_lists'



class ToDoDetailView(DetailView):
    model = ToDoListModel
    # form_class = TaskDetailForm
    template_name = 'planer/todolist_detail.html'


# ToDoLists
class CreateToDoListView(CreateView):
    model = ToDoListModel
    form_class = ToDoListCreateForm
    template_name = 'planer/todolist_create_form.html'

    def get_initial(self):
        return {
            'user': self.request.user,
        }
    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})



class TaskDeleteView(DeleteView):
    model = ToDoListModel

