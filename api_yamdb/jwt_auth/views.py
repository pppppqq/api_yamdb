from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UsernameEmailSerializer, TokenByCodeSerializer
from .services import ConfirmationCodeService


User = get_user_model()


class SignUpView(APIView):
    """
    Регистрирует пользователя и отправляет код подтверждения на email.
    """

    def post(self, request):
        serializer = UsernameEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        ConfirmationCodeService.generate_and_send_code(user)

        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK
        )


class TokenByCodeView(APIView):
    """
    Принимает код подтверждения и выдаёт JWT-токен.
    """

    def post(self, request):
        serializer = TokenByCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']

        if not ConfirmationCodeService.validate_code(username, code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )

        access = AccessToken.for_user(username)

        return Response(
            {'token': str(access)},
            status=status.HTTP_200_OK
        )
