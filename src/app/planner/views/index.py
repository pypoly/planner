from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.planner.models import ToDoListModel


class IndexView(LoginRequiredMixin, ListView):
    model = ToDoListModel
    template_name = 'planer/index.html'
    context_object_name = 'todolists_lists'

    def get_queryset(self):
        qs = ToDoListModel.objects.filter(user=self.request.user)
        if self.request.GET.get('archived') == '1':
            return qs.filter(archived=True).order_by('-created_at')
        return qs.filter(archived=False).order_by('-created_at')
