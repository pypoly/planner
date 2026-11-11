"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tempfile import template

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views import View
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from app.planner.views import (
    IndexView,
    CreateToDoListView,
    ToDoDetailView,
    ToDoListUpdateView,
    TodoListDeleteView,
    ToDoUnarchiveView,
    CreateTaskView,
    UpdateTaskView,
    DeleteTaskView,
    TaskToggleView,
)
from app.users.forms import PlannerAuthenticationForm
from app.users.views import RegisterUser, UserProfileView

urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateToDoListView.as_view(), name='create'),
    path('detail/<int:pk>/', ToDoDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ToDoListUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TodoListDeleteView.as_view(), name='delete'),
    path('unarchive/<int:pk>/', ToDoUnarchiveView.as_view(), name='unarchive'),
    path('create_task/<int:pk>/', CreateTaskView.as_view(), name='create_task'),
    path('update_task/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('toggle_task/<int:pk>/', TaskToggleView.as_view(), name='toggle_task'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile' ),
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
            authentication_form=PlannerAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/', include('app.planner.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', include('app.admin_panel.urls', namespace='adm'))

]

