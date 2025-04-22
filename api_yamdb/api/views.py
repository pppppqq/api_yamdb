from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Comment, Genre, Review, Title
from .filters import TitleFilter
from .mixins import GenreCategoryMixin, ReadOnlyOrAdminPermissionMixin
from .permissions import IsAuthorModeratorAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями (Comment)."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(
            author=self.request.user,
            review=review
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами (Review)."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdmin
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(
    ReadOnlyOrAdminPermissionMixin,
    viewsets.ModelViewSet
):
    """ViewSet для работы с произведениями (Title)."""

    queryset = (
        Title.objects.annotate(
            rating=Round(Avg('reviews__score'))
        )
        .select_related('category')
        .prefetch_related('genre')
        .order_by(*Title._meta.ordering)
    )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering_fields = ('name', 'year', 'rating')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class GenreViewSet(
    ReadOnlyOrAdminPermissionMixin,
    GenreCategoryMixin
):
    """ViewSet для работы с жанрами (Genre)."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(
    ReadOnlyOrAdminPermissionMixin,
    GenreCategoryMixin
):
    """ViewSet для работы с категориями (Category)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
