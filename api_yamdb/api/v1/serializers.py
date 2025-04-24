from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import CustomUser
from users.validators import validate_username_is_allowed
from reviews.constants import MAX_NAME_LENGTH, MAX_EMAIL_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_is_allowed),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
        help_text='Обязательное поле. Не более 254 символов.'
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        errors = {}

        user_by_email = CustomUser.objects.filter(email=email).first()
        user_by_username = CustomUser.objects.filter(username=username).first()

        if user_by_email != user_by_username:
            if user_by_email:
                errors['email'] = 'Этот email уже занят.'
            if user_by_username:
                errors['username'] = 'Этот username уже занят.'

        if errors:
            raise ValidationError(errors)
        return data


class TokenByCodeSerializer(serializers.Serializer):
    """
    Сериализатор авторизации: принимает username и код подтверждения.
    """

    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_is_allowed),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    confirmation_code = serializers.CharField(
        required=True,
        help_text='Код подтверждения для аутентификации.'
    )


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для администраторов и суперпользователей с доступом
    ко всем полям модели пользователя.
    """

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class AuthUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обычных пользователей: роль только для чтения.
    """

    class Meta:
        model = CustomUser
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
