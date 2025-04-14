from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

# создание базовой модели

db = SQLAlchemy()  # Создайте объект db здесь

from core.database.repository.loan_repository import LoanRepository
from core.database.repository.user_repository import UserRepository


def init_db(app):
       with app.app_context():
           db.create_all()  # Создает все таблицы, определенные в ваших моделях.


def init_db(app, db):
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            logging.exception(f"Ошибка при создании таблиц базы данных: {e}") #Более корректная обработка ошибки

def init_app(app, db, migrate):
    try:
        db.init_app(app)
        migrate.init_app(app, db)
    except Exception as e:
        logging.exception(f"Ошибка при инициализации расширений: {e}") #Более корректная обработка ошибки