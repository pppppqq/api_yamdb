from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from api.validators import validate_username_not_me


User = get_user_model()


# api/serializers.py


class UsernameEmailSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=(EmailValidator(),),
        help_text='Обязательное поле. Не более 254 символов.'
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        errors = {}

        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        if user_by_email != user_by_username:
            if user_by_email:
                errors['email'] = 'Этот email уже занят.'
            if user_by_username:
                errors['username'] = 'Этот username уже занят.'

        if errors:
            raise serializers.ValidationError(errors)

        return data


class TokenByCodeSerializer(serializers.Serializer):
    """
    Сериализатор авторизации: принимает username и код подтверждения.
    """

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    confirmation_code = serializers.CharField(
        required=True,
        help_text='Код подтверждения для аутентификации.'
    )

    def validate_username(self, value):
        try:
            return User.objects.get(username=value)
        except ObjectDoesNotExist:
            raise NotFound(detail={'username': 'Пользователь не найден.'})
