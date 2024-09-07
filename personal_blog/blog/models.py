from django.db import models
from users.models import User


class Post(models.Model):
    '''Модель для постов пользователей'''

    PUBLISHED = 'published'
    NOT_PUBLISHED = 'not_published'

    POST_STATUS = (
        (NOT_PUBLISHED, 'Не опубликовано'),
        (PUBLISHED, 'Опубликовано'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор поста'
    )
    post_name = models.CharField(
        max_length=32,
        verbose_name='Имя записи',
    )
    post_text = models.TextField(
        max_length=256,
        verbose_name='Текст поста',
    )
    created = models.DateTimeField(auto_now_add=True)
    post_status = models.CharField(
        max_length=15,
        choices=POST_STATUS,
        default=NOT_PUBLISHED,
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.post_name
