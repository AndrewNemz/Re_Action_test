'''from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
import json
from django.test import Client
from ..models import Post
from ..serializers import PostSerializer

from users.models import User


class APIPostTest(TestCase):
    def setUp(self):
        self.user = self.client.post('http://127.0.0.1:8000/api/users/', data={
            "username": "test user",
            "first_name": "test_name",
            "last_name": "test last_name",
            "password": "test password",
            "email": "test@mail.ru"
        })
        response = self.client.post('http://127.0.0.1:8000/api/auth/token/login/', data={
            "email": "test@mail.ru",
            "password": "test password"
        })
        self.token = response.data["auth_token"]

    def test_create_posts(self):
        headers = {"Authorization": f"Token {self.token}"}
        valid_data = {
            'post_name': 'valid_test_post_name',
            'post_text': 'valid_test_post_text',
        }
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)'''

