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
from django.contrib import admin
from django.urls import path

from app.planer.forms.todo import ToDoListUpdateForm
from app.planer.views import IndexView, CreateToDoListView, ToDoDetailView
from app.planer.views.todo import ToDoListUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateToDoListView.as_view(), name='create'),
    path('detail/<int:pk>/', ToDoDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ToDoListUpdateView.as_view(), name='update'),

]
