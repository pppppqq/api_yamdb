from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Отзыв', help_text='Введите текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        help_text='Оцените от 1 до 10'
    )
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
from django.utils import timezone

from reviews import constants


class Title(models.Model):
    """Модель произведения (фильм, книга и т.д.)."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH,
        db_index=True
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)],
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-year', 'name']

    def __str__(self):
        return f'{self.name} ({self.year})'


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=constants.LENGTH_SLUG
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=constants.LENGTH_SLUG
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
