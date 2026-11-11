from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app.planner.models import TaskModel, TaskStatus, ToDoListModel


class TodoViewsTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='pass1234')
        self.u2 = User.objects.create_user('u2', password='pass1234')
        self.todo1 = ToDoListModel.objects.create(title='Todo one', user=self.u1)
        self.todo2 = ToDoListModel.objects.create(title='Todo two', user=self.u2)
        self.task1 = TaskModel.objects.create(name='Task one', tasklist=self.todo1)

    def test_anonymous_redirected_to_login(self):
        for url in (reverse('index'), reverse('detail', args=[self.todo1.pk]),
                    reverse('create'), reverse('update', args=[self.todo1.pk])):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login', response['Location'])

    def test_index_lists_only_own_todos(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Todo one')
        self.assertNotContains(response, 'Todo two')

    def test_detail_own_todo(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_other_todo_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_update_other_todo_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('update', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_delete_other_todo_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.post(reverse('delete', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_create_todo_assigns_user(self):
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('create'), {'title': 'New', 'description': ''})
        self.assertEqual(ToDoListModel.objects.get(title='New').user, self.u1)

    def test_create_todo_ignores_user_post(self):
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('create'), {
            'title': 'Sneaky', 'description': '', 'user': self.u2.pk,
        })
        self.assertEqual(ToDoListModel.objects.get(title='Sneaky').user, self.u1)

    def test_archive_and_unarchive(self):
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('delete', args=[self.todo1.pk]))
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.archived)
        self.client.post(reverse('unarchive', args=[self.todo1.pk]))
        self.todo1.refresh_from_db()
        self.assertFalse(self.todo1.archived)

    def test_unarchive_other_todo_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.post(reverse('unarchive', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_archived_tab(self):
        self.todo1.archived = True
        self.todo1.save(update_fields=['archived'])
        self.client.login(username='u1', password='pass1234')
        active = self.client.get(reverse('index'))
        archived = self.client.get(reverse('index') + '?archived=1')
        self.assertNotContains(active, 'Todo one')
        self.assertContains(archived, 'Todo one')

    def test_detail_hides_canceled_by_default(self):
        TaskModel.objects.create(
            name='Canceled task', tasklist=self.todo1, status=TaskStatus.CANCELED
        )
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        self.assertNotContains(response, 'Canceled task')

    def test_detail_status_filter_shows_canceled(self):
        TaskModel.objects.create(
            name='Canceled task', tasklist=self.todo1, status=TaskStatus.CANCELED
        )
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(
            reverse('detail', args=[self.todo1.pk]) + '?status=3'
        )
        self.assertContains(response, 'Canceled task')

    def test_index_page_uses_planner_layout(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'planner/css/planner.css')
        self.assertContains(response, 'Новая цель')
        self.assertContains(response, reverse('detail', args=[self.todo1.pk]))

    def test_index_page_shows_archive_tab(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('index'))
        self.assertContains(response, '?archived=1')

    def test_detail_page_has_task_actions(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        self.assertContains(response, 'planner/css/planner.css')
        self.assertContains(response, reverse('toggle_task', args=[self.task1.pk]))
        self.assertContains(response, reverse('create_task', args=[self.todo1.pk]))
        self.assertContains(response, reverse('update', args=[self.todo1.pk]))

    def test_detail_page_shows_task_name(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        self.assertContains(response, 'Task one')

    def test_form_pages_use_planner_layout(self):
        self.client.login(username='u1', password='pass1234')
        urls = [
            reverse('create'),
            reverse('update', args=[self.todo1.pk]),
            reverse('delete', args=[self.todo1.pk]),
            reverse('create_task', args=[self.todo1.pk]),
            reverse('update_task', args=[self.task1.pk]),
            reverse('delete_task', args=[self.task1.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)
            self.assertContains(response, 'planner/css/planner.css')

    def test_todo_create_form_has_title_field(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('create'))
        self.assertContains(response, 'name="title"')

    def test_detail_toolbar_has_add_then_search(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        html = response.content.decode()
        add_url = reverse('create_task', args=[self.todo1.pk])
        self.assertLess(html.index(add_url), html.index('<form method="get"'))
        self.assertIn('nb-btn-sm', html)
        self.assertIn('task-search-checkbox', html)
        self.assertIn('task-search-panel', html)

    def test_detail_search_panel_opens_when_filter_active(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(
            reverse('detail', args=[self.todo1.pk]) + '?q=Task'
        )
        html = response.content.decode()
        self.assertRegex(html, r'id="taskSearchToggle"[^>]*checked')

    def test_brand_links_home(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('detail', args=[self.todo1.pk]))
        self.assertContains(response, 'class="brand-link"')
        self.assertContains(response, 'href="%s"' % reverse('index'))

    def test_update_pages_have_back_link(self):
        self.client.login(username='u1', password='pass1234')
        for url in (
            reverse('update', args=[self.todo1.pk]),
            reverse('update_task', args=[self.task1.pk]),
        ):
            response = self.client.get(url)
            self.assertContains(response, 'fa-arrow-left', msg_prefix=url)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='pass1234')
        self.u2 = User.objects.create_user('u2', password='pass1234')
        self.todo1 = ToDoListModel.objects.create(title='T1', user=self.u1)
        self.todo2 = ToDoListModel.objects.create(title='T2', user=self.u2)
        self.task1 = TaskModel.objects.create(name='Task one', tasklist=self.todo1)
        self.task2 = TaskModel.objects.create(name='Task two', tasklist=self.todo2)

    def test_create_task_assigns_owned_todo(self):
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('create_task', args=[self.todo1.pk]), {
            'name': 'New task', 'description': '', 'status': TaskStatus.PENDING,
        })
        self.assertEqual(TaskModel.objects.get(name='New task').tasklist, self.todo1)

    def test_create_task_ignores_tasklist_post(self):
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('create_task', args=[self.todo1.pk]), {
            'name': 'Sneaky task', 'description': '', 'status': TaskStatus.PENDING,
            'tasklist': self.todo2.pk,
        })
        self.assertEqual(TaskModel.objects.get(name='Sneaky task').tasklist, self.todo1)

    def test_create_task_other_todo_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('create_task', args=[self.todo2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_update_other_task_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('update_task', args=[self.task2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_delete_other_task_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.post(reverse('delete_task', args=[self.task2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_own_task(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.post(reverse('toggle_task', args=[self.task1.pk]))
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, TaskStatus.DONE)
        self.assertRedirects(response, reverse('detail', args=[self.todo1.pk]))

    def test_toggle_other_task_404(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.post(reverse('toggle_task', args=[self.task2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_canceled_is_noop(self):
        self.task1.status = TaskStatus.CANCELED
        self.task1.save(update_fields=['status'])
        self.client.login(username='u1', password='pass1234')
        self.client.post(reverse('toggle_task', args=[self.task1.pk]))
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, TaskStatus.CANCELED)
