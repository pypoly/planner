from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthPagesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'u1', password='pass1234', email='u1@example.com'
        )

    def test_login_page_uses_planner_layout(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'planner/css/planner.css')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'class="nb-input"')
        self.assertNotContains(response, reverse('logout'))

    def test_profile_page_uses_planner_layout(self):
        self.client.login(username='u1', password='pass1234')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'planner/css/planner.css')
        self.assertContains(response, 'Данные профиля')
        self.assertContains(response, 'Смена пароля')
        self.assertContains(response, reverse('index'))
        self.assertContains(response, 'name="profile-username"')
        self.assertContains(response, 'name="password-old_password"')
