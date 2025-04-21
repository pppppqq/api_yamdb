from django.contrib import admin

from .models import (
    Title,
    Genre,
    Category,
    Review,
    Comment
)


class TitleAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Title (Произведения)."""

    list_display = ('name', 'year', 'category')
    list_filter = ('year', 'category')
    search_fields = ('name', 'description')
    filter_horizontal = ('genre',)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Genre (Жанры)."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class CategoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Category (Категории)."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ReviewAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Review (Отзывы)."""

    list_display = ('author', 'title', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class CommentAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Comment (Комментарии)."""

    list_display = ('author', 'review', 'created')
    list_filter = ('created',)
    search_fields = ('text', 'author__username')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
