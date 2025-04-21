from django.db.models import Avg
from django.db.models.functions import Round
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Comment, Review, Category, Genre, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'created')
        read_only_fields = ('author', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        read_only_fields = ('author', 'title')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_slug(self, value):
        """Проверяет уникальность slug жанра."""

        if Genre.objects.filter(slug=value).exists():
            raise ValidationError('Жанр с таким slug уже существует.')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        """Проверяет уникальность slug категории."""

        if Category.objects.filter(slug=value).exists():
            raise ValidationError('Категория с таким slug уже существует.')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title с расчетом рейтинга."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        write_only=False,
        required=True,
        help_text="Список slug'ов жанров"
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        write_only=False,
        required=True,
        help_text="Slug категории"
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        """Вычисляет средний рейтинг на основе отзывов"""
        result = obj.reviews.aggregate(
            rating=Round(Avg('score'))
        )
        return int(result['rating']) if result['rating'] is not None else None

    def validate_year(self, value):
        """Проверяет, что год выпуска не больше текущего"""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f'Год выпуска ({value}) не может быть больше текущего'
                f'({current_year})'
            )
        return value

    def to_representation(self, instance):
        """Кастомизация вывода для GET-запросов."""
        data = super().to_representation(instance)
        if not self.context.get('writing', False):
            data['genre'] = GenreSerializer(
                instance.genre.all(), many=True
            ).data
            data['category'] = CategorySerializer(instance.category).data
        return data
