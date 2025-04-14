from core.utils.date_time import * # Импорт всех функций из date_time.py
from core.utils.currency import * # Импорт всех функций из currency.py
from core.utils.validation import * # Импорт всех функций из validation.py
from core.utils.crypto import * # Импорт всех функций из crypto.py
from core.utils.logging import configure_logging # Импорт функции настройки логирования
from .date_time import get_current_timestamp


def init_app(app):
    configure_logging(app) # Настройка логирования для приложения
