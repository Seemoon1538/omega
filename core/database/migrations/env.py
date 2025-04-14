import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
import os
DATABASE_URL = "postgresql://admin:1029Rikka@127.0.0.1:5432/omega_db"
if DATABASE_URL is None:
      raise ValueError("DATABASE_URL environment variable is not set.")

# Абсолютный путь к файлу env.py
env_file_path = os.path.dirname(__file__)

# Путь к папке core
core_path = os.path.abspath(os.path.join(env_file_path, "..", ".."))

# Добавляем путь к core в sys.path
sys.path.append(core_path)

# Создаем engine и Base
engine = create_engine(DATABASE_URL)
Base = declarative_base()
target_metadata = Base.metadata


config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("postgresql://admin:1029Rikka@127.0.0.1:5432/omega_db")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()