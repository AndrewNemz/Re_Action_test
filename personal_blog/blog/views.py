from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Post
from .serializers import PostSerializer


@extend_schema(
    request=PostSerializer,
    responses={200: PostSerializer(many=True)},
    methods=["POST", "GET"]
)
class APIPost(APIView):
    '''
    Класс для создания постов. И получения всех постов.
    Действия доступны для зарегестрированных пользователей.
    '''

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


@extend_schema(
        request=PostSerializer,
        methods=["PATCH", "GET"],
        responses={
            200: PostSerializer(many=True),
            400: OpenApiResponse(
                description='Bad request (something invalid)'
            ),
        },
    )
class APIPostDetail(APIView):
    '''
    Класс для получения конкретно выбранного поста,
    для его редактирования или удаления.
    Действия PATCH, DELETE доступны для автора поста или для администратора.
    '''

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

    @extend_schema(
        request=PostSerializer,
        methods=["DELETE"],
        responses={
            204: OpenApiResponse(description='Have been deleted, no content'),
            400: OpenApiResponse(
                description='Bad request (something invalid)'
            ),
        },
    )
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
