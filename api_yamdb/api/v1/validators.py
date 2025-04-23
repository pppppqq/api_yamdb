from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


def validate_username_not_me(value):
    """Проверяет, что имя пользователя не 'me'."""
    if value.lower() == 'me':
        raise ValidationError(
            _("Username '%(value)s' is not allowed."),
            params={"value": value},
        )


def validate_unique_username_email(username, email):
    """Проверяет уникальность пары username и email."""
    User = get_user_model()

    errors = {}

    user_by_email = User.objects.filter(email=email).first()
    user_by_username = User.objects.filter(username=username).first()

    if user_by_email != user_by_username:
        if user_by_email:
            errors['email'] = 'Этот email уже занят.'
        if user_by_username:
            errors['username'] = 'Этот username уже занят.'

    if errors:
        raise ValidationError(errors)
