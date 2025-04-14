import hashlib
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_secure_token(length=32):
    """Генерирует безопасный токен заданной длины."""
    token = os.urandom(length)
    return base64.urlsafe_b64encode(token).decode('utf-8')


def hash_password(password, salt):
    """Хеширует пароль с использованием PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def generate_salt():
    """Генерирует случайную соль."""
    return os.urandom(16)


def hash_data(data):
    """Вычисляет SHA-256 хэш данных."""
    hasher = hashlib.sha256()
    hasher.update(data.encode())
    return hasher.hexdigest()
