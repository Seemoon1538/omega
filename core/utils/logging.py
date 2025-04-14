import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    """Настраивает логирование для приложения Flask."""

    log_dir = app.config.get('LOG_DIR', 'logs')  # Используем LOG_DIR из конфигурации или 'logs' по умолчанию
    os.makedirs(log_dir, exist_ok=True)  # Создаем директорию для логов, если ее нет

    log_file = os.path.join(log_dir, 'app.log')  # Путь к лог-файлу

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5) # 10MB, 5 backups

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.config['DEBUG'] else logging.INFO)
