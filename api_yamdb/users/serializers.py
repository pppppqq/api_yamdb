from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username может содержать только буквы, цифры и @/./+/-/_'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value
