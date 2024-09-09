from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.test import Client

from ..models import Post
from ..serializers import PostSerializer


class APIPostTest(TestCase):
    def setUp(self):
        self.user = self.client.post(
            '/api/users/',
            data={
                "username": "test user",
                "first_name": "test_name",
                "last_name": "test last_name",
                "password": "test password",
                "email": "test@mail.ru"
            }
        )
        response = self.client.post(
            '/api/auth/token/login/',
            data={
                "email": "test@mail.ru",
                "password": "test password"
            }
        )
        self.token = response.data["auth_token"]
        self.valid_data = {
            'post_name': 'valid_test_post_name',
            'post_text': 'valid_test_post_text',
        }

    def test_create_posts_from_authorized_user(self):
        posts_count = Post.objects.count()
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_create_posts_from_unauthorized_user(self):
        posts_count = Post.objects.count()
        guest_client = Client()
        response = guest_client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_create_invalid_posts_from_authorized_user(self):
        posts_count = Post.objects.count()
        headers = {"Authorization": f"Token {self.token}"}
        invalid_data = {
            'post_text': 'valid_test_post_text',
        }
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=invalid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_get_posts(self):
        headers = {"Authorization": f"Token {self.token}"}
        self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        response = self.client.get(reverse('blog:post_get_posts'))
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_posts(self):
        headers = {"Authorization": f"Token {self.token}"}
        self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        response = self.client.get(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 10})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIPostDetailTest(TestCase):
    def setUp(self):
        self.user = self.client.post(
            '/api/users/',
            data={
                "username": "test user",
                "first_name": "test_name",
                "last_name": "test last_name",
                "password": "test password",
                "email": "test@mail.ru"
            }
        )
        response = self.client.post(
            '/api/auth/token/login/',
            data={
                "email": "test@mail.ru",
                "password": "test password"
            }
        )
        self.token = response.data["auth_token"]
        self.valid_data = {
            'post_name': 'valid_test_post_name',
            'post_text': 'valid_test_post_text',
        }
        self.another_valid_data = {
            'post_name': 'another_valid_test_post_name',
            'post_text': 'another_valid_test_post_text',
        }
        self.expected_output = 'another_valid_test_post_name'

    def test_delete_post_from_authorized_user(self):
        posts_count = Post.objects.count()
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 1}),
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(posts_count, 0)

    def test_delete_post_from_unauthorized_user(self):
        posts_count = Post.objects.count()
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 1}),
            headers=None
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), posts_count+1)

    def test_patch_post_from_authorized_user(self):
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.patch(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 1}),
            data=self.another_valid_data,
            content_type='application/json',
            headers=headers
        )
        post = Post.objects.get(pk=1)
        serializer = PostSerializer(post)
        self.assertEqual(serializer.data['post_name'], self.expected_output)

    def test_patch_post_from_unauthorized_user(self):
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.patch(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 1}),
            data=self.another_valid_data,
            content_type='application/json',
            headers=None
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_post_invalid_data(self):
        headers = {"Authorization": f"Token {self.token}"}
        response = self.client.post(
            reverse('blog:post_get_posts'),
            data=self.valid_data,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.patch(
            reverse('blog:get_delete_patch_posts', kwargs={'pk': 1}),
            data=self.expected_output,
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
