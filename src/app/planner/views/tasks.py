from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.planner.forms.tasks import CreateTaskForm, UpdateTaskForm, DeleteTaskForm
from app.planner.models import TaskModel, ToDoListModel, TaskStatus


class CreateTaskView(CreateView):
    model = TaskModel
    form_class = CreateTaskForm
    template_name = 'planer/tasks/tasks_create_form.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.tasklist.pk})


    def get_initial(self):
        todo = ToDoListModel.objects.get(pk=self.kwargs['pk'])
        return {
            'tasklist': todo,
        }

class UpdateTaskView(UpdateView):
    model = TaskModel
    form_class = UpdateTaskForm
    template_name = 'planer/tasks/task_update_form.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.tasklist.pk})

class DeleteTaskView(DeleteView):
    model = TaskModel
    template_name = 'planer/tasks/task_delete.html'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        tasklist_pk = obj.tasklist.pk
        obj.status = TaskStatus.CANCELED
        obj.save()
        return redirect(reverse('detail', kwargs={'pk': tasklist_pk}))

    # def get_success_url(self):
    #     return reverse('detail', kwargs={'pk': self.object.tasklist.pk})