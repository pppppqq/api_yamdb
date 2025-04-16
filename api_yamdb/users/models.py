from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email', max_length=150, unique=True
    )
    bio = models.TextField(verbose_name='О себе', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
