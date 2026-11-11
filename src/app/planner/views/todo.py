from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from app.planner.forms.todo import ToDoListCreateForm, ToDoListUpdateForm
from app.planner.models import ToDoListModel, TaskStatus


class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDoListModel
    template_name = 'planer/todo/todolist_detail.html'
    context_object_name = 'todo'

    def get_queryset(self):
        return ToDoListModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        status = self.request.GET.get('status')
        if status in {'1', '2', '3'}:
            tasks = tasks.filter(status=status)
        else:
            tasks = tasks.exclude(status=TaskStatus.CANCELED)
        q = self.request.GET.get('q')
        if q:
            tasks = tasks.filter(name__icontains=q)
        ctx['tasks'] = tasks.order_by('order', 'created_at')
        ctx['status_choices'] = TaskStatus.choices()
        return ctx


class CreateToDoListView(LoginRequiredMixin, CreateView):
    model = ToDoListModel
    form_class = ToDoListCreateForm
    template_name = 'planer/todo/todolist_create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class ToDoListUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoListModel
    form_class = ToDoListUpdateForm
    template_name = 'planer/todo/todolist_update_form.html'

    def get_queryset(self):
        return ToDoListModel.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class TodoListDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoListModel
    template_name = 'planer/todo/todolist_delete.html'

    def get_queryset(self):
        return ToDoListModel.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.archived = True
        self.object.save(update_fields=['archived'])
        return redirect(reverse('index'))


class ToDoUnarchiveView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(ToDoListModel, pk=pk, user=request.user)
        todo.archived = False
        todo.save(update_fields=['archived'])
        return redirect(reverse('detail', kwargs={'pk': todo.pk}))
