from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserChangeForm
from django.views.generic.edit import CreateView

from app import users
from app.admin_panel.forms.user import UserPasswordForm, UserUpdateForm
from app.planner.models import TaskModel, TaskStatus, ToDoListModel
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

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )

        is_active = self.request.GET.get('is_active')
        if is_active == '1':
            queryset = queryset.filter(is_active=True)
        elif is_active == '0':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('-date_joined')

class UserDetailView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/user_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        ctx['user_obj'] = user
        ctx['form_change_password'] = UserPasswordForm(prefix='passwd')
        ctx['form_change_user'] = UserUpdateForm(instance=user, prefix='user')
        return ctx

    def post(self, request, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if 'btn_passwd' in request.POST:
            form = UserPasswordForm(request.POST, prefix='passwd')
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('adm:user_detail', pk=user.pk)
            ctx = self.get_context_data()
            ctx['form_change_password'] = form
            return self.render_to_response(ctx)
        elif 'btn_user' in request.POST:
            form = UserUpdateForm(request.POST, instance=user, prefix='user')
            if form.is_valid():
                form.save()
                return redirect('adm:user_detail', pk=user.pk)
            ctx = self.get_context_data()
            ctx['form_change_user'] = form
            return self.render_to_response(ctx)
        return self.render_to_response(self.get_context_data())

class StatisticUserView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/statistic.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_count'] = User.objects.count()
        ctx['todo_count'] = ToDoListModel.objects.count()
        ctx['todo_active'] = ToDoListModel.objects.filter(archived=False).count()
        ctx['todo_archived'] = ToDoListModel.objects.filter(archived=True).count()
        ctx['task_count'] = TaskModel.objects.count()

        status_choices = [(int(value), label) for value, label in TaskStatus.choices()]
        ctx['task_status_labels'] = [label for _, label in status_choices]
        ctx['task_status_counts'] = [
            TaskModel.objects.filter(status=value).count() for value, _ in status_choices
        ]
        return ctx
