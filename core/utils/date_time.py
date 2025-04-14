import datetime


def get_current_datetime():
    """Возвращает текущую дату и время в формате ISO 8601."""
    return datetime.datetime.utcnow().isoformat() + 'Z'


def format_datetime(dt, format="%Y-%m-%d %H:%M:%S"):
    """Форматирует дату и время в указанный формат."""
    return dt.strftime(format)


def parse_datetime(datetime_str, format="%Y-%m-%d %H:%M:%S"):
    """Преобразует строку в объект datetime."""
    try:
        return datetime.datetime.strptime(datetime_str, format)
    except ValueError:
        return None


def get_current_timestamp():
    from time import time
    return int(time())  # Возвращает Unix timestamp в секундах