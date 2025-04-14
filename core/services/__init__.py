from flask import Blueprint
from core.security.authorization import bp
from core.blueprints.loan import loan_blueprint
from core.blueprints.investment import investment_blueprint
from core.blueprints.chat import chat_blueprint
from core.blueprints.news import news_blueprint
from core.blueprints.message import message_blueprint
from core.blueprints.notification import notification_blueprint
from core.blueprints.poll import poll_blueprint
from core.blueprints.transaction import transaction_blueprint
from core.blueprints.platform import platform_blueprint
from core.blueprints.user import user_blueprint
import logging
import inspect

def register_blueprints(app):
    """Регистрирует все Blueprint'ы сервисов в приложении Flask."""
    blueprints = [
        user_blueprint,
        loan_blueprint,
        investment_blueprint,
        transaction_blueprint,
        notification_blueprint,
        chat_blueprint,
        message_blueprint,
        poll_blueprint,
        news_blueprint,
        platform_blueprint,
    ]
    for blueprint in blueprints:
        try:
            app.register_blueprint(blueprint)
        except ImportError as e:
            file_path = getattr(blueprint, '__file__', 'Unknown')  #Обработка отсутствия атрибута __file__
            logging.getLogger(__name__).exception(f"Ошибка импорта Blueprint'а {blueprint.name} из {file_path}: {e}")
        except Exception as e:
            file_path = getattr(blueprint, '__file__', 'Unknown') #Обработка отсутствия атрибута __file__
            logging.getLogger(__name__).exception(f"Ошибка регистрации Blueprint'а {blueprint.name} из {file_path} с URL-префиксом {blueprint.url_prefix}: {e}")