from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class APIPost(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class APIPostDetail(APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = self.request.user
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data)
        if user != serializer.instance.author and not user.is_admin:
            return Response(
                {'error': 'Нельзя изменять чужой контент'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            if not user.is_admin:
                serializer.save(author=self.request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            serializer.save(author=serializer.instance.author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.request.user
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data)
        if user != serializer.instance.author and not user.is_admin:
            return Response(
                {'error': 'Нельзя удалять чужой контент'},
                status=status.HTTP_400_BAD_REQUEST
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
