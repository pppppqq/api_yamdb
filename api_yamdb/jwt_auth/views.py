from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import SignUpSerializer, TokenByCodeSerializer


User = get_user_model()


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Ваш код подтверждения',
            message=f'Код: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK
        )


class TokenByCodeView(APIView):
    def post(self, request):
        serializer = TokenByCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']

        if not default_token_generator.check_token(user, code):
            raise serializers.ValidationError(
                {'Ошибка': 'Неверный код подтверждения.'}
            )

        access = AccessToken.for_user(user)

        return Response(
            {'token': str(access)},
            status=status.HTTP_200_OK
        )
