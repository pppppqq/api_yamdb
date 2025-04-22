from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидатор: год не должен превышать текущий."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Год не может быть больше текущего ({current_year}).'
        )
