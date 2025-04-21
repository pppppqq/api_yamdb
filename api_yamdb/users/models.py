from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями: email, bio и роль.
    Используется для аутентификации, регистрации и управления правами доступа.
    """

    email = models.EmailField(
        verbose_name='email', max_length=254, unique=True
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
        ordering = ('username',)

    def save(self, *args, **kwargs):
        if self._state.adding and self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
