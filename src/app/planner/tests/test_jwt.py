from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class JWTAuthAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'ADFRhhdk@123'
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.list_url = reverse('task-list')
        self.token_url = reverse('token_obtain_pair')  # /api/token/

    def get_jwt_token(self, username=None, password=None):
        """Get access-token"""
        response = self.client.post(
            self.token_url,
            {'username': username or self.username,
             'password': password or self.password},
            format='json',
        )
        return response

    def test_unauthorized_request(self):
        """Without token 401"""
        self.client.credentials()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_success(self):
        """Successfully obtain access token 200"""
        response = self.get_jwt_token()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_wrong_password(self):
        """Invalid password fail 401"""
        response = self.get_jwt_token(password='wrong')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_request_with_jwt(self):
        """With jwt token 200"""
        token_response = self.get_jwt_token()
        access = token_response.data.get('access')
        self.assertIsNotNone(access)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_rejected(self):
        """With invalid token 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        """Update access token using refresh token"""
        token_response = self.get_jwt_token()
        refresh = token_response.data['refresh']

        refresh_url = reverse('token_refresh')  # /api/token/refresh/
        response = self.client.post(refresh_url, {'refresh': refresh}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def tearDown(self):
        self.client.credentials()