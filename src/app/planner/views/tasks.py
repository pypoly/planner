from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.planner.forms.tasks import CreateTaskForm, UpdateTaskForm
from app.planner.models import TaskModel, ToDoListModel, TaskStatus


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = TaskModel
    form_class = CreateTaskForm
    template_name = 'planer/tasks/tasks_create_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.todo = None
        if request.user.is_authenticated:
            self.todo = get_object_or_404(
                ToDoListModel, pk=self.kwargs['pk'], user=request.user
            )

    def form_valid(self, form):
        form.instance.tasklist = self.todo
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.todo.pk})


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = TaskModel
    form_class = UpdateTaskForm
    template_name = 'planer/tasks/task_update_form.html'

    def get_queryset(self):
        return TaskModel.objects.filter(tasklist__user=self.request.user)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.tasklist_id})


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = TaskModel
    template_name = 'planer/tasks/task_delete.html'

    def get_queryset(self):
        return TaskModel.objects.filter(tasklist__user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = TaskStatus.CANCELED
        self.object.save(update_fields=['status'])
        return redirect(reverse('detail', kwargs={'pk': self.object.tasklist_id}))


class TaskToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(
            TaskModel, pk=pk, tasklist__user=request.user
        )
        if task.status != TaskStatus.CANCELED:
            if task.status == TaskStatus.DONE:
                task.status = TaskStatus.PENDING
            else:
                task.status = TaskStatus.DONE
            task.save(update_fields=['status'])
        return redirect(reverse('detail', kwargs={'pk': task.tasklist_id}))
