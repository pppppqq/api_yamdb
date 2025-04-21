from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import AdminUserSerializer, AuthUserSerializer
from api.permissions import IsAdminOrSuperuser


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления пользователями.

    - Администраторы могут просматривать, создавать, редактировать
    и удалять пользователей.

    - Авторизованные пользователи могут получать и обновлять
    свои данные через эндпоинт /me/.
    """

    http_method_names = ('get', 'post', 'patch', 'delete')

    queryset = User.objects.all()
    lookup_field = 'username'

    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('username',)

    def get_permissions(self):
        """
        Возвращает права доступа в зависимости от действия.
        Для /me/ — только авторизованные пользователи.
        Для остальных — админы или суперпользователи.
        """
        if self.action == 'me':
            return (IsAuthenticated(),)
        return (IsAuthenticated(), IsAdminOrSuperuser())

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        Для /me/ — AuthUserSerializer.
        Для остальных — AdminUserSerializer.
        """
        if self.action == 'me':
            return AuthUserSerializer
        return AdminUserSerializer

    @action(detail=False, methods=('get', 'patch', 'delete'))
    def me(self, request, *args, **kwargs):
        """
        Эндпоинт /users/me/ для работы с собственным профилем пользователя.

        GET — получение данных текущего пользователя.
        PATCH — частичное обновление данных.
        DELETE — метод не поддерживается.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
