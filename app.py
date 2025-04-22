import sys
import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig, TestingConfig, ProductionConfig  # Импорты конфигов
from core.database import db, init_db
from core.utils import configure_logging
from core.security import auth_service
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
from routes import user
from core.database.repository.user_repository import UserRepository

app = Flask('omega')
logging.basicConfig(filename='C:\\app.log', level=logging.DEBUG)
          
@app.route('/auth/login', methods=['POST'])
def login():
    try:
                  data = request.get_json()
                  app.logger.debug('Received: %s', data)
                  username = data.get('username')
                  password = data.get('password')
                  if username == 'test' and password == 'test':
                    return {'status': 'success', 'message': 'Logged in'}, 200
                    return {'status': 'error', 'message': 'Invalid credentials'}, 401
    except Exception as e:
                app.logger.error('Error: %s', str(e))
                return {'status': 'error', 'message': 'Server error'}, 500
          
@app.route('/test')
def test():
            return 'OK'

# Определение словаря конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def create_app(config_name):
    app = Flask('omega')  # Исправлено: name → __name__
    if config_name not in config:
        logging.error(f"Недопустимое имя конфигурации: {config_name}. Доступные: {list(config.keys())}")
        raise ValueError(f"Недопустимое имя конфигурации: {config_name}")
    
    app.config.from_object(config[config_name])  # Загружаем конфигурацию
    logging.info(f"Конфигурация загружена: {config_name}")

    try:
        db.init_app(app)
        auth_service.init_app(app)
        configure_logging(app)
        CORS(app)
        app.register_blueprint(bp)

        # Регистрация blueprints
        app.register_blueprint(user_blueprint)
        app.register_blueprint(loan_blueprint)
        app.register_blueprint(investment_blueprint)
        app.register_blueprint(transaction_blueprint)
        app.register_blueprint(notification_blueprint)
        app.register_blueprint(chat_blueprint)
        app.register_blueprint(message_blueprint)
        app.register_blueprint(poll_blueprint)
        app.register_blueprint(news_blueprint)
        app.register_blueprint(platform_blueprint)

        with app.app_context():
            user_repository = UserRepository(db)
            user.user_repository = user_repository
            init_db(app, db)

    except Exception as e:
        logging.error(f"Ошибка при создании приложения: {e}", exc_info=True)
        return None

    return app

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение имени конфигурации
config_name = os.getenv('FLASK_CONFIG', 'development')  # Исправлено: or → ,
logging.info(f"Используемая конфигурация: {config_name}")

# Создание приложения
app = create_app(config_name)

if __name__ == '__main__':  # Исправлено: name → __name__ и main → __main__
    if app:
        app.run(debug=app.config.get('DEBUG', False))
