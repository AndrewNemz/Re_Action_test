from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    '''Сериализатор для постов пользователей'''

    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'post_name',
            'post_text',
            'created',
            'post_status'
        )
