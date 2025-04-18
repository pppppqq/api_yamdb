from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist

from users.serializers import AdminUserSerializer


User = get_user_model()


class SignUpSerializer(AdminUserSerializer):

    def validate(self, data):
        email = data['email']
        username = data['username']

        try:
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    {'Ошибка': 'Email уже зарегистрирован с другим username'}
                )
            return data

        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {'Ошибка': 'Этот username уже занят'}
                )
            return data


class TokenByCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        try:
            return User.objects.get(username=value)
        except ObjectDoesNotExist:
            raise NotFound(detail={'Ошибка': 'Пользователь не найден'})
