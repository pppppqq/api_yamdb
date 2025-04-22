from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsAdminOrSuperuser
from .serializers import AdminUserSerializer, AuthUserSerializer


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

    permission_classes = (IsAuthenticated, IsAdminOrSuperuser)
    serializer_class = AdminUserSerializer

    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
        serializer_class=AuthUserSerializer
    )
    def me(self, request, *args, **kwargs):
        """
        Эндпоинт /users/me/ для работы с собственным профилем пользователя.

        GET — получение данных текущего пользователя.
        PATCH — частичное обновление данных.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
