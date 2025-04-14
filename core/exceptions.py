class OmegaException(Exception):
    """Базовый класс для исключений платформы Omega."""
    def __init__(self, message: str = ""):
        super().__init__(message)
        self.status_code = 500


class AuthenticationError(OmegaException):
    """Ошибка аутентификации."""
    def __init__(self, message: str = "Ошибка аутентификации"):
        super().__init__(message)
        self.status_code = 401


class AuthorizationError(OmegaException):
    """Ошибка авторизации."""
    def __init__(self, message: str = "Ошибка авторизации"):
        super().__init__(message)
        self.status_code = 403


class ValidationError(OmegaException):
    """Ошибка валидации данных."""
    def __init__(self, message: str = "Ошибка валидации данных"):
        super().__init__(message)
        self.status_code = 400


class NotFoundError(OmegaException):
    """Ресурс не найден."""
    def __init__(self, message: str = "Ресурс не найден"):
        super().__init__(message)
        self.status_code = 404


class DatabaseError(OmegaException):
    """Ошибка работы с базой данных."""
    def __init__(self, message: str = "Ошибка работы с базой данных"):
        super().__init__(message)
        self.status_code = 500


class BusinessLogicError(OmegaException):
    """Ошибка бизнес-логики."""
    def __init__(self, message: str = "Ошибка бизнес-логики"):
        super().__init__(message)
        self.status_code = 400


class PaymentError(OmegaException):
    """Ошибка платёжной системы."""
    def __init__(self, message: str = "Ошибка платёжной системы"):
        super().__init__(message)
        self.status_code = 500


class BlockchainError(OmegaException):
    """Ошибка работы с блокчейном."""
    def __init__(self, message: str = "Ошибка работы с блокчейном"):
        super().__init__(message)
        self.status_code = 500


class UserAlreadyExistsError(OmegaException):
    """Пользователь уже существует."""
    def __init__(self, message: str = "Пользователь уже существует"):
        super().__init__(message)
        self.status_code = 409


class UserNotFoundError(OmegaException):
    """Пользователь не найден."""
    def __init__(self, message: str = "Пользователь не найден"):
        super().__init__(message)
        self.status_code = 404


class IncorrectPasswordError(OmegaException):
    """Неверный пароль."""
    def __init__(self, message: str = "Неверный пароль"):
        super().__init__(message)
        self.status_code = 401


class InvalidCredentialsError(OmegaException):
    """InvalidCredentialsError."""
    def __init__(self, message: str = "InvalidCredentialsError"):
        super().__init__(message)
        self.status_code = 201


class WeakPasswordError(OmegaException):
    """WeakPasswordError."""
    def __init__(self, message: str = "WeakPasswordError"):
        super().__init__(message)
        self.status_code = 202        


class InvalidEmailError(OmegaException):
    """InvalidEmailError."""
    def __init__(self, message: str = "InvalidEmailError"):
        super().__init__(message)
        self.status_code = 203            


class InvalidUsernameError(OmegaException):
    """InvalidUsernameError."""
    def __init__(self, message: str = "InvalidUsernameError"):
        super().__init__(message)
        self.status_code = 204                    