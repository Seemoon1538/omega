from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy # Импортируем SQLAlchemy явно

# Создаем экземпляр SQLAlchemy.  Лучше делать это в app.py или другом файле инициализации
db = SQLAlchemy()


# Инициализация расширений
migrate = Migrate()
mail = Mail()
cors = CORS()
ma = Marshmallow()


def initialize_extensions(app):
    """Инициализирует все расширения Flask."""
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app)
    ma.init_app(app)