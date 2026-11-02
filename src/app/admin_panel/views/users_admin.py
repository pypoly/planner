from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserChangeForm
from django.views.generic.edit import CreateView

from app import users
from app.admin_panel.forms.user import UserPasswordForm, UserUpdateForm
from app.planner.models import ToDoListModel
from django.contrib.auth.forms import PasswordChangeForm


class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class UserListView(StaffRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admin_panel/users.html'
    paginate_by = 15

class UserDetailView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/user_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        ctx['form_change_password'] = UserPasswordForm(prefix='passwd')
        ctx['form_change_user'] = UserUpdateForm(instance=user, prefix='user')
        return ctx

    def post(self, request, **kwargs ):
        if 'btn_passwd' in request.POST:
            form = UserPasswordForm(request.POST, prefix='passwd')
            if form.is_valid():
                user = User.objects.get(pk=self.kwargs['pk'])
                user.set_password(form.cleaned_data['password'])
                user.save()
        elif 'btn_user' in request.POST:
            user = User.objects.get(pk=self.kwargs['pk'])
            form = UserUpdateForm(request.POST, instance=user, prefix='user')
            if form.is_valid():
                form.save()
        return self.render_to_response(self.get_context_data())

class StatisticUserView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/statistic.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_count = User.objects.count()
        ctx['user_count'] = user_count
        todo_count = ToDoListModel.objects.count()
        ctx['todo_count'] = todo_count
        return ctx



