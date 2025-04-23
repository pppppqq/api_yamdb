from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from rest_framework import filters, mixins, permissions, viewsets, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS

from .permissions import IsAdminOrSuperuser
from .validators import validate_username_not_me
from reviews.constants import MAX_NAME_LENGTH, MAX_EMAIL_LENGTH


class ReadOnlyOrAdminPermissionMixin:
    """Миксин прав доступа."""

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAdminOrSuperuser(),)


class UsernameEmailMixin(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
        validators=(EmailValidator(),),
        help_text='Обязательное поле. Не более 254 символов.'
    )


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
