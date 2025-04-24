from django.core.exceptions import ValidationError
from django.conf import settings


def validate_username_is_allowed(value):
    """Проверяет, что имя пользователя разрешено."""
    if value.lower() in settings.PROHIBITED_NICKNAMES:
        raise ValidationError(
            f'Username {value.lower()} запрещен.'
        )
