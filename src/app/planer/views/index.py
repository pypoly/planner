from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from app.planer.models import ToDoListModel


class IndexView(ListView):
    model = ToDoListModel
    template_name ='planer/index.html'
    context_object_name = 'todolists_lists'

    def get_queryset(self):
        q = super().get_queryset()
        if self.request.user.is_authenticated:
            q: QuerySet = q.active().filter(user=self.request.user)
        else:
            q = ToDoListModel.objects.none()
        return q

