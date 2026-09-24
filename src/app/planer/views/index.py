from django.views.generic import ListView

from app.planer.models import ToDoListModel


class IndexView(ListView):
    model = ToDoListModel
    template_name ='planer/index.html'
    context_object_name = 'todolists_lists'

