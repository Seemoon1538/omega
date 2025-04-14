import re
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    """Проверяет, является ли строка допустимым адресом электронной почты."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_valid_username(username):
    """Проверяет, является ли строка допустимым именем пользователя."""
    # Проверка на длину и допустимые символы (можно настроить под свои нужды)
    if not 3 <= len(username) <= 30:
        return False
    if not re.fullmatch(r"^[a-zA-Z0-9_]+$", username):
        return False
    return True


def is_valid_password(password):
    """Проверяет, является ли строка допустимым паролем."""
    # Проверка на длину и сложность (можно настроить под свои нужды)
    if len(password) < 8:
        return False
    #Добавьте другие проверки сложности пароля, например, наличие заглавных букв, цифр и специальных символов.
    return True


def is_valid_amount(amount):
    """Проверяет, является ли строка допустимым числом."""
    try:
        float(amount)
        return True
    except ValueError:
        return False
