from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS

from .permissions import IsAdminOrSuperuser


class ReadOnlyOrAdminPermissionMixin:
    """Миксин прав доступа."""

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAdminOrSuperuser(),)


class GenreCategoryMixin(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """Миксин для жанров и категорий (только list, create, delete)."""

    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
