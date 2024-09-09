from django.test import TestCase
from freezegun import freeze_time

from ..models import Post
from ..serializers import PostSerializer

from users.models import User


@freeze_time('2024-09-08')
class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test@mail.ru',
        )
        self.post = Post.objects.create(
            author=self.user,
            post_name='test_post_name',
            post_text='test_post_text',
            created='2024-09-08T00:00:00Z'
        )
        self.serializer = PostSerializer(self.post)

    def test_serializer_valid_data(self):
        '''Проверка сериализатора на валидность.'''
        data = {
            'author': self.user,
            'post_name': 'test_post_name',
            'post_text': 'test_post_text'
        }
        self.serializer = PostSerializer(data=data)
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_output(self):
        '''Проверка сериализатора на ожидаемые данные'''
        expected_output = {
            'id': self.post.id,
            'author': 'test_user',
            'post_name': 'test_post_name',
            'post_text': 'test_post_text',
            'created': '2024-09-08T00:00:00Z',
            'post_status': 'not_published'
        }
        self.assertEqual(self.serializer.data, expected_output)
