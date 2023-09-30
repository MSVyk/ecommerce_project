from django.core.exceptions import ValidationError

def validate_password_contains_uppercase(value):
    if not any(char.isupper() for char in value):
        raise ValidationError("The password must contain at least one uppercase letter.")