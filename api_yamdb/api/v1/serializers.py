from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from reviews.constants import MAX_NAME_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title
from .mixins import UsernameEmailMixin
from .validators import (
    validate_username_not_me,
    validate_unique_username_email
)


User = get_user_model()


class SignUpSerializer(UsernameEmailMixin, serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    def validate(self, data):
        validate_unique_username_email(
            username=data.get('username'),
            email=data.get('email')
        )
        return data


class TokenByCodeSerializer(serializers.Serializer):
    """
    Сериализатор авторизации: принимает username и код подтверждения.
    """

    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    confirmation_code = serializers.CharField(
        required=True,
        help_text='Код подтверждения для аутентификации.'
    )

    def validate_username(self, value):
        try:
            return User.objects.get(username=value)
        except ObjectDoesNotExist:
            raise NotFound(detail={'username': ['Пользователь не найден.']})


class AdminUserSerializer(UsernameEmailMixin, serializers.ModelSerializer):
    """
    Сериализатор для администраторов и суперпользователей с доступом
    ко всем полям модели пользователя.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate(self, data):
        validate_unique_username_email(
            username=data.get('username'),
            email=data.get('email')
        )
        return data


class AuthUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обычных пользователей: роль только для чтения.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    pub_date = serializers.DateTimeField(
        source='created',
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        """
        Валидатор на ограничение количества отзывов.

        Пользователь может оставлять только
        один отзыв к одному произведению.
        """

        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists():
                raise ValidationError(
                    "Можно оставить только один отзыв на произведение."
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        help_text="Список slug'ов жанров"
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
        help_text="Slug категории"
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category'
        )

    def to_representation(self, instance):
        """Используем сериализатор для чтения после сохранения."""
        return TitleReadSerializer(instance, context=self.context).data
