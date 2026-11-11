from django.test import TestCase

from app.planner.forms.tasks import CreateTaskForm, UpdateTaskForm
from app.planner.forms.todo import ToDoListCreateForm, ToDoListUpdateForm


class PlannerFormsTest(TestCase):
    def test_todo_forms_exclude_user(self):
        self.assertNotIn('user', ToDoListCreateForm().fields)
        self.assertNotIn('user', ToDoListUpdateForm().fields)

    def test_task_forms_exclude_tasklist(self):
        self.assertNotIn('tasklist', CreateTaskForm().fields)
        self.assertNotIn('tasklist', UpdateTaskForm().fields)

    def test_date_fields_use_date_input(self):
        self.assertEqual(
            ToDoListCreateForm().fields['start_date'].widget.attrs.get('type'), 'date'
        )
        self.assertEqual(
            CreateTaskForm().fields['deadline'].widget.attrs.get('type'), 'date'
        )
