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
