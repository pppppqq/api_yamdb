from django.contrib.auth import get_user_model
from django.db import models

from reviews import constants
from .validators import validate_year

User = get_user_model()


class Title(models.Model):
    """Модель произведения (фильм, книга и т.д.)."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH,
        db_index=True
    )
    year = models.SmallIntegerField(
        'Год выпуска',
        validators=(validate_year,),
        db_index=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанры',
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
        ordering = ('-year', 'name')

    def __str__(self):
        return f'Произведение: "{self.name}" (год: {self.year})'


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Идентификатор (slug)',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return f'Жанр: {self.name}'


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        'Название',
        max_length=constants.MAX_LENGTH
    )
    slug = models.SlugField(
        'Идентификатор (slug)',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return f'Категория: {self.name}'


class Review(models.Model):
    """Модель отзывов произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        'Отзыв',
        help_text='Введите текст отзыва'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        help_text='Оцените от 1 до 10'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)


class Comment(models.Model):
    """Модель комментариев произведения."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)
