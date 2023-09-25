from rest_framework import viewsets
from django.core.exceptions import PermissionDenied
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Запрещено измененять чужие посты!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Запрещено удалять чужие данные!')
        super(PostViewSet, self).perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        if not self.request.user:
            raise PermissionDenied(
                'Неавторизованным пользователям запрещено оствлять комментарии'
            )
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(pk=self.kwargs.get("post_id"))
        )

    def perform_update(self, serializer):
        if not self.request.user:
            raise PermissionDenied(
                'Неавторизованным пользователям запрещено изменять комментарии'
            )
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Запрещено изменять чужие кмментарии')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user:
            raise PermissionDenied(
                'Неавторизованным пользователям запрещено удалять комментарии'
            )
        if instance.author != self.request.user:
            raise PermissionDenied('Запрещено удалять чужие данные!')
        super(CommentViewSet, self).perform_destroy(instance)
