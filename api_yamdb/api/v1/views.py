from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import GenreCategoryMixin, ReadOnlyOrAdminPermissionMixin
from .permissions import IsAdminOrSuperuser, IsAuthorModeratorAdmin
from .serializers import (
    AdminUserSerializer,
    AuthUserSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenByCodeSerializer,
    SignUpSerializer
)
from .services import ConfirmationCodeService


User = get_user_model()


class SignUpView(APIView):
    """
    Регистрирует пользователя и отправляет код подтверждения на email.
    """

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        ConfirmationCodeService.generate_and_send_code(user)

        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK
        )


class TokenByCodeView(APIView):
    """
    Принимает код подтверждения и выдаёт JWT-токен.
    """

    def post(self, request):
        serializer = TokenByCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']

        if not ConfirmationCodeService.validate_code(username, code):
            raise serializers.ValidationError({
                'confirmation_code': ['Неверный код подтверждения.']
            })

        access = AccessToken.for_user(username)

        return Response(
            {'token': str(access)},
            status=status.HTTP_200_OK
        )


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


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями (Comment)."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorModeratorAdmin)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title_id=self.kwargs['title_id']
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
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

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
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
