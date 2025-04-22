from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from rest_framework import serializers

from api.validators import validate_username_not_me
from reviews.constants import MAX_NAME_LENGTH, MAX_EMAIL_LENGTH


User = get_user_model()

# api/serializers.py


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для администраторов и суперпользователей с доступом
    ко всем полям модели пользователя.
    """

    username = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=(UnicodeUsernameValidator(), validate_username_not_me),
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_'
        )
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
        validators=(EmailValidator(),),
        help_text='Обязательное поле. Не более 254 символов.'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
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


class AuthUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обычных пользователей: роль только для чтения.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
