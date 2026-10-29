from django.urls import path

from app.admin_panel.views.task_admin import TaskUpdateView
from app.admin_panel.views.users_admin import StatisticUserView, UserListView, UserDetailView
from app.admin_panel.views.todo_admin import ToDoListView, ToDoDetailView, ToDoUpdateView

app_name = 'admin_panel'
urlpatterns = [
    path('', StatisticUserView.as_view(), name='statistic'),
    path('todo-list', ToDoListView.as_view(), name='index'),
    path('todo-detail/<int:pk>/', ToDoDetailView.as_view(), name='todo_detail'),
    path('task-update/<int:pk>', TaskUpdateView.as_view(), name='task_update'),
    path('todo-update/<int:pk>', ToDoUpdateView.as_view(), name='todo_update'),
    path('user-list/', UserListView.as_view(), name='users'),
    path('user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),


# path('user_todo_list/<int:pk>', UserTasksView.as_view(), name = 'user_tasks'),

    ]
