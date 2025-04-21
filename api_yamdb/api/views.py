from rest_framework import viewsets
# permissions, status,
#  from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


from api.serializers import CommentSerializer, ReviewSerializer
from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from reviews.models import Comment, Review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs['review_id']
        )

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .filters import TitleFilter
from .permissions import AdminPermissions
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с произведениями (Title)."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminPermissions]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering_fields = ('name', 'year', 'rating')


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с жанрами (Genre)."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminPermissions]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с категориями (Category)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminPermissions]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
