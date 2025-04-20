from django.core.validators import MaxValueValidator
from django.db import models
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
