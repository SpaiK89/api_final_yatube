from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrReadOnly
from posts.models import Post, Comment, Group


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет создания, редактирования, удаления, просмотра кверисета постов
    или отдельного поста"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """функция добавления текущего пользователя,
        как автора поста при создании"""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет просмотра кверисета созданных в проекте групп"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет создания, редактирования, удаления, просмотра кверисета
    комментариев или отдельного комментария, принадлежащего определенному
    посту"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get("post_id"))

    def get_queryset(self):
        """Функция определения конкретного поста, к которому
        принадлежат комментарии/должен быть создан комментарий"""
        new_queryset = Comment.objects.filter(post=self.get_post())
        return new_queryset

    def perform_create(self, serializer):
        """Функция добавления текущего пользователя, как автора
        комментария конкретного поста при создании нового комментария"""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Вьюсет создания, и просмотра кверисета авторов, на которых подписан
    текущий пользователь"""
    serializer_class = FollowSerializer
    # http_method_names = ['get', 'post', 'head']
    # хорошая штука, но по ТЗ мы не можем просматривать отдельный объект,
    # приходится использовать миксины
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        """Функция получения списка авторов, на которых подписан
        текущий пользователь"""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Функция добавления текущего пользователя, как подписчика
        при подписке на нового автора"""
        serializer.save(user=self.request.user)
