from django.views.generic import UpdateView

from app.admin_panel.forms.tasks import TaskUpdateForm
from app.planner.forms.tasks import UpdateTaskForm
from app.planner.models import TaskModel


class TaskUpdateView(UpdateView):
    model = TaskModel
    form_class = TaskUpdateForm
    context_object_name = 'task'
    template_name = 'admin_panel/task_update.html'