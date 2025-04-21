from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, RegexValidator
from rest_framework import serializers


User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для администраторов и суперпользователей с доступом
    ко всем полям модели пользователя.
    """

    email = serializers.EmailField(
        validators=[
            MaxLengthValidator(
                254,
                message='Email должен быть не длиннее 254 символов.'),
        ]
    )
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=(
                    'Username может содержать только буквы, цифры и @/./+/-/_'
                )
            ),
            MaxLengthValidator(
                150,
                message='Username должен быть не длиннее 150 символов.'
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        """
        Проверка уникальности username и email.
        """
        username = data.get('username')
        email = data.get('email')

        queryset = User.objects.all()

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if username and queryset.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'Этот username уже занят.'}
            )

        if email and queryset.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                {'email': 'Этот email уже занят.'}
            )

        return data

    def validate_username(self, value):
        """
        Запрещает использовать "me" в качестве username.
        """
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class AuthUserSerializer(AdminUserSerializer):
    """
    Сериализатор для обычных пользователей: роль только для чтения.
    """

    role = serializers.ReadOnlyField()
