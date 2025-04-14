import hashlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.exceptions import InvalidSignature


def generate_rsa_key_pair(key_size=2048):
    """Генерирует пару ключей RSA."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key, password=None, encoding='PEM'):
    """Сериализует приватный ключ RSA."""
    return private_key.private_bytes(
        encoding=getattr(serialization, encoding),
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption() if password is None else serialization.BestAvailableEncryption(password.encode())
    )


def serialize_public_key(public_key, encoding='PEM'):
    """Сериализует публичный ключ RSA."""
    return public_key.public_bytes(
        encoding=getattr(serialization, encoding),
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def deserialize_private_key(key_bytes, password=None, encoding='PEM'):
    """Десериализует приватный ключ RSA."""
    return serialization.load_pem_private_key(key_bytes, password=password.encode() if password else None, backend=default_backend())


def deserialize_public_key(key_bytes, encoding='PEM'):
    """Десериализует публичный ключ RSA."""
    return serialization.load_pem_public_key(key_bytes, backend=default_backend())


def sign_data(data, private_key):
    """Подписывает данные приватным ключом RSA."""
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()


def verify_signature(data, signature, public_key):
    """Проверяет подпись данных публичным ключом RSA."""
    signature_bytes = base64.b64decode(signature.encode())
    try:
        public_key.verify(
            signature_bytes,
            data,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def generate_hash(data):
    """Генерирует SHA-256 хеш данных."""
    hasher = hashlib.sha256()
    hasher.update(data.encode('utf-8'))
    return hasher.hexdigest()


from cryptography.hazmat.primitives import padding