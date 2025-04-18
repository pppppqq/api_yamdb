from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BaseUserSerializer
from .permissions import IsAdminOrSuperuser


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser,)

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = BaseUserSerializer

    pagination_class = PageNumberPagination
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('username',)
