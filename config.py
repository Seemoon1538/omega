from datetime import timedelta
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    """Базовая конфигурация приложения."""
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'YOUR_PLACEHOLDER_SECRET_KEY')  # Исправлено: os.environ.get → os.getenv
    DATABASE_URL: str = os.getenv('DATABASE_URL')  # Исправлено: os.environ.get → os.getenv
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL if DATABASE_URL else 'sqlite:///:memory:'  # Добавлена защита от None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    MAIL_SERVER: Optional[str] = os.getenv('MAIL_SERVER')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', '25'))  # Добавлены кавычки для значения по умолчанию
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS', '0').lower() in ('true', '1')
    MAIL_USERNAME: Optional[str] = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: Optional[str] = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: Optional[str] = os.getenv('MAIL_DEFAULT_SENDER')
    IDENTITY_VERIFICATION_API_KEY: Optional[str] = os.getenv('IDENTITY_VERIFICATION_API_KEY')
    IDENTITY_VERIFICATION_API_URL: Optional[str] = os.getenv('IDENTITY_VERIFICATION_API_URL')
    FILE_STORAGE_API_KEY: Optional[str] = os.getenv('FILE_STORAGE_API_KEY')
    FILE_STORAGE_API_URL: Optional[str] = os.getenv('FILE_STORAGE_API_URL')
    PAYMENT_GATEWAY_API_KEY: Optional[str] = os.getenv('PAYMENT_GATEWAY_API_KEY')
    PAYMENT_GATEWAY_API_URL: Optional[str] = os.getenv('PAYMENT_GATEWAY_API_URL')
    MODERATION_API_KEY: Optional[str] = os.getenv('MODERATION_API_KEY')
    MODERATION_API_URL: Optional[str] = os.getenv('MODERATION_API_URL')
    NOTIFICATION_API_KEY: Optional[str] = os.getenv('NOTIFICATION_API_KEY')
    NOTIFICATION_API_URL: Optional[str] = os.getenv('NOTIFICATION_API_URL')
    BLOCKCHAIN_NODE_URL: Optional[str] = os.getenv('BLOCKCHAIN_NODE_URL')
    BLOCKCHAIN_PRIVATE_KEY: Optional[str] = os.getenv('BLOCKCHAIN_PRIVATE_KEY')
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(days=30)
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SAMESITE: str = "Strict"
    SESSION_COOKIE_HTTPONLY: bool = True

class DevelopmentConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True
    DATABASE_URL: str = os.getenv('DATABASE_URL_DEV', 'sqlite:///:memory:')
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL  # Переопределяем, чтобы учесть DATABASE_URL_DEV
    SESSION_COOKIE_SECURE: bool = False

class ProductionConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False

class TestingConfig(Config):
    TESTING: bool = True
    DATABASE_URL: str = os.getenv('DATABASE_URL_TEST', 'sqlite:///:memory:')
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL  # Переопределяем для тестов
    SESSION_COOKIE_SECURE: bool = False

# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
