from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username_not_me(value):
    if value.lower() == 'me':
        raise ValidationError(
            _("Username '%(value)s' is not allowed."),
            params={"value": value},
        )
