from http import HTTPStatus

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .permissions import IsAdminOrSuperuser


class ReadOnlyOrAdminPermissionMixin(viewsets.ModelViewSet):
    """Миксин прав доступа."""
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAdminOrSuperuser(),)


class GenreCategoryMixin(viewsets.ModelViewSet):
    """Миксин для моделей жанра и категории"""
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ('get', 'post', 'delete')

    def retrieve(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
