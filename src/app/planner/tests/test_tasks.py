import datetime

from django.tasks import Task
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from app.planner.models import TaskModel, TaskStatus, ToDoListModel


class TasksAPITestCase(APITestCase):

    def setUp(self):
        """Set up testing data objects"""
        self.user = User.objects.create_user(username='test', password='pass1234')
        self.client.force_authenticate(user=self.user)
        self.todolist = ToDoListModel.objects.create(
            title='ToDo1',
            description='test description',
            user=self.user,
        )

        self.task = TaskModel.objects.create(
            name='test1',
            description='description1',
            start_date=datetime.datetime(2020, 1, 1),
            end_date=datetime.datetime(2020, 1, 2),
            order=1,
            status=TaskStatus.PENDING,
            deadline=datetime.datetime(2020, 1, 3),
            tasklist=self.todolist,
        )
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.id])
        self.valid_payload = {
            'name': 'правильно',
            'description': 'правильное описание',
            'order': 1,
            'tasklist': self.todolist.id,
        }
        self.invalid_payload = {
            'name': '',
            'description': 1,
        }

    def test_get_list(self):
        """GET /tasks/ — list tasks"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'test1')

    def test_get_detail(self):
        """GET /tasks/<id>/ single task"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test1')

    def test_create_task(self):
        """POST /tasks/ — create task"""
        response = self.client.post(self.list_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskModel.objects.count(), 2)
        self.assertEqual(TaskModel.objects.last().name, self.valid_payload['name'])

    def test_create_book_invalid(self):
        """POST /tasks/ with invalid data"""
        response = self.client.post(self.list_url, self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_update_task(self):
        """PUT /tasks/<id>/ full update task"""
        response = self.client.put(self.detail_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'правильно')

    def test_delete_book(self):
        """DELETE /tasks/<id>/ delete task"""
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskModel.objects.count(), 0)
