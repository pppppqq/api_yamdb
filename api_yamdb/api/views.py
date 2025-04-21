from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from http import HTTPStatus


from reviews.models import Category, Genre, Title, Comment, Review
from .mixins import ReadOnlyOrAdminPermissionMixin
from .permissions import IsAuthorModeratorAdmin
from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями (Comment)."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(
            author=self.request.user,
            review=review
        )

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами (Review)."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class TitleViewSet(ReadOnlyOrAdminPermissionMixin):
    """ViewSet для работы с произведениями (Title)."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering_fields = ('name', 'year', 'rating')
    http_method_names = ['get', 'post', 'patch', 'delete']


class GenreViewSet(ReadOnlyOrAdminPermissionMixin):
    """ViewSet для работы с жанрами (Genre)."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


class CategoryViewSet(ReadOnlyOrAdminPermissionMixin):
    """ViewSet для работы с категориями (Category)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
