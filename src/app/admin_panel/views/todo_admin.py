from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import UpdateView, DetailView
from django.views.generic.list import ListView

from app.admin_panel.forms.todos import ToDoUpdateForm
from app.planner.models import TaskModel, TaskStatus, ToDoListModel


class ToDoListView(ListView):
    model = ToDoListModel
    context_object_name = 'todo_list'
    template_name = 'admin_panel/todo-list.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')

        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(title__icontains=query)

        archived = self.request.GET.get('archived')
        if archived == 'active':
            queryset = queryset.filter(archived=False)
        elif archived == 'archived':
            queryset = queryset.filter(archived=True)

        return queryset.order_by('-created_at')


class ToDoDetailView(DetailView):
    model = ToDoListModel
    context_object_name = 'todo'
    template_name = 'admin_panel/todo-detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        todo_list_pk = self.kwargs['pk']
        tasks = TaskModel.objects.filter(tasklist_id=todo_list_pk).order_by('order', 'created_at')

        query = self.request.GET.get('q', '').strip()
        if query:
            tasks = tasks.filter(name__icontains=query)

        status = self.request.GET.get('status')
        if status:
            if int(status) in TaskStatus:
                tasks = tasks.filter(status=status)

        paginator = Paginator(tasks, 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        ctx['page_obj'] = page_obj
        ctx['tasks'] = page_obj.object_list
        return ctx


class ToDoUpdateView(UpdateView):
    model = ToDoListModel
    form_class = ToDoUpdateForm
    context_object_name = 'todo'
    template_name = 'admin_panel/todo-update.html'

    def get_success_url(self):
        return reverse('adm:todo_detail', kwargs={'pk': self.object.pk})
