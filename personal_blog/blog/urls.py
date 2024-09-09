from django.urls import path

from .views import APIPost, APIPostDetail


app_name = 'blog'

urlpatterns = [
    path('posts/', APIPost.as_view(), name='post_get_posts'),
    path(
        'posts/<int:pk>/',
        APIPostDetail.as_view(),
        name='get_delete_patch_posts'
    ),
]
