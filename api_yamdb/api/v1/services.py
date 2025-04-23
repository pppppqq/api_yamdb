from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


class ConfirmationCodeService:
    """
    Сервис для работы с кодами подтверждения пользователя.
    Генерирует и отправляет код подтверждения на указанные контактные данные.
    """

    @staticmethod
    def generate_code(user):
        """
        Генерирует код подтверждения для пользователя с использованием
        стандартного токен-генератора.
        """
        return default_token_generator.make_token(user)

    @staticmethod
    def send_confirmation_code_email(user, code):
        """
        Отправляет код подтверждения на email пользователя.
        """
        send_mail(
            subject='Ваш код подтверждения',
            message=f'Код: {code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

    @classmethod
    def generate_and_send_code(cls, user):
        """
        Генерирует и отправляет код подтверждения пользователю.
        """
        code = cls.generate_code(user)
        cls.send_confirmation_code_email(user, code)
        return code

    @staticmethod
    def validate_code(user, code):
        """
        Проверяет корректность кода подтверждения для пользователя.
        """
        return default_token_generator.check_token(user, code)
