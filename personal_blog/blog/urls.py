from django.urls import path

from .views import APIPost, APIPostDetail


app_name = 'blog'

urlpatterns = [
    path('posts/', APIPost.as_view()),
    path('posts/<int:pk>/', APIPostDetail.as_view()),
]
