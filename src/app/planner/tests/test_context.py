from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from app.planner.context_processors import global_stats
from app.planner.models import TaskModel, TaskStatus, ToDoListModel


class GlobalStatsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u1', password='x')
        self.todo = ToDoListModel.objects.create(title='t', user=self.user)
        TaskModel.objects.create(name='a', tasklist=self.todo, status=TaskStatus.DONE)
        TaskModel.objects.create(name='b', tasklist=self.todo, status=TaskStatus.PENDING)
        TaskModel.objects.create(name='c', tasklist=self.todo, status=TaskStatus.CANCELED)

    def _request(self, user):
        request = RequestFactory().get('/')
        request.user = user
        return request

    def test_counts_exclude_canceled(self):
        self.assertEqual(
            global_stats(self._request(self.user)),
            {'global_total': 2, 'global_done': 1},
        )

    def test_anonymous_empty(self):
        self.assertEqual(
            global_stats(self._request(AnonymousUser())),
            {'global_total': 0, 'global_done': 0},
        )

    def test_archived_lists_excluded(self):
        self.todo.archived = True
        self.todo.save(update_fields=['archived'])
        self.assertEqual(
            global_stats(self._request(self.user)),
            {'global_total': 0, 'global_done': 0},
        )

    def test_model_helpers_exclude_canceled(self):
        self.assertEqual(self.todo.task_total, 2)
        self.assertEqual(self.todo.task_done, 1)


class TaskStatusLabelsTest(TestCase):
    def test_russian_labels(self):
        labels = dict(TaskStatus.choices())
        self.assertEqual(labels[TaskStatus.PENDING], 'В ожидании')
        self.assertEqual(labels[TaskStatus.DONE], 'Выполнено')
        self.assertEqual(labels[TaskStatus.CANCELED], 'Отменено')
