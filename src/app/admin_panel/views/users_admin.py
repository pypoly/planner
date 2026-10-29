from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserChangeForm

from app.admin_panel.forms.user import UserUpdateForm
from app.planner.models import ToDoListModel


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin_panel/users.html'

class UserDetailView(UpdateView):
    model = User
    form_class = UserUpdateForm
    context_object_name = 'user'
    template_name = 'admin_panel/user_detail.html'




class StatisticUserView(TemplateView):
    template_name = 'admin_panel/statistic.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_count = User.objects.count()
        ctx['user_count'] = user_count
        todo_count = ToDoListModel.objects.count()
        ctx['todo_count'] = todo_count
        return ctx



