from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#  Здесь должна быть ваша строка подключения к базе данных
DATABASE_URL = 'postgresql://admin:1029Rikka@127.0.0.1:5432/omega_db' # Замените на ваши данные

engine = create_engine(DATABASE_URL)
Base = declarative_base()