import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


def generate_key(password, salt):
    """Генерирует ключ шифрования Fernet из пароля и соли."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt(data, key):
    """Шифрует данные с использованием ключа Fernet."""
    f = Fernet(key)
    return f.encrypt(data.encode())


def decrypt(encrypted_data, key):
    """Расшифровывает данные с использованием ключа Fernet."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()


def generate_salt():
    """Генерирует случайную соль."""
    return os.urandom(16)