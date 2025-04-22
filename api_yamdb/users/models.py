from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from reviews.constants import MAX_NAME_LENGTH, MAX_LENGTH
from api.validators import validate_username_not_me


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями: email, bio и роль.
    Используется для аутентификации, регистрации и управления правами доступа.
    """

    class RoleChoises(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=MAX_NAME_LENGTH,
        unique=True,
        validators=(
            UnicodeUsernameValidator(),
            validate_username_not_me
        )
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_LENGTH,
        choices=RoleChoises.choices,
        default=RoleChoises.USER
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'Пользователь: {self.username}, Email: {self.email}'

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.is_superuser or self.role == self.RoleChoises.ADMIN

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == self.RoleChoises.MODERATOR
