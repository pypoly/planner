from django.views.generic import CreateView, ListView, DetailView, DeleteView

from app.planer.forms import ToDoListCreateForm, TaskDetailForm
from app.planer.models import TaskModel

# Tasks
class TaskListView(ListView):
    model = TaskModel
    template_name ='planer/index.html'
    context_object_name = 'task_list'

class CreateTaskView(CreateView):
    model = TaskModel
    form_class = ToDoListCreateForm
    template_name = 'planer/task_create_form.html'

    def get_initial(self):
        return {
            'user': self.request.user,
        }

class TaskDetailView(DetailView):
    model = TaskModel
    form_class = TaskDetailForm
    template_name = 'planer/task_detail.html'


class TaskDeleteView(DeleteView):
    model = TaskModel

