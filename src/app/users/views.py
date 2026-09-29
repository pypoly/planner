from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.users.forms import UserRegisterForm


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')
    #
    # def get(self, request:HttpRequest, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('index')
    #     return super().get(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, TemplateView):
    # model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_profile'] = UserProfileForm(prefix='profile', instance=self.request.user)
        ctx['form_password'] = MyPasswordChangeForm(user=self.request.user, prefix='password')
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        ctx = self.get_context_data()
        if action == 'password':
            form = MyPasswordChangeForm(data=self.request.POST, user=self.request.user, prefix='password')
            if form.is_valid():
                form.save()
            else:
                # print(form.errors.as_text())
                ctx['form_password'] = form
        elif action == 'profile':
            form = UserProfileForm(request.POST, prefix='profile', instance=self.request.user)
            if form.is_valid():
                form.save()
            else:
                # print(form.errors.as_text())
                ctx['form_profile'] = form
        return render(request, self.template_name, ctx)


    def get(self, request:HttpRequest, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('planer:index')
        return super().get(request, *args, **kwargs)