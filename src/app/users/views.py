from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.users.forms import UserRegisterForm


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    # template_name = 'planer/register.html'
    success_url = reverse_lazy('login')

    def get(self, request:HttpRequest, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('planer:index')
        return super().get(request, *args, **kwargs)