from flask import session, jsonify, abort, current_app
from flask_login import login_required as flask_login_required
from functools import wraps
from core.database.repository.user_repository import UserRepository
from werkzeug.security import check_password_hash
from core.exceptions import AuthenticationError, UserNotFoundError, IncorrectPasswordError
from datetime import timedelta
from core.database import db
from core.utils.response import make_response
from sqlalchemy.exc import SQLAlchemyError


def init_app(app):
    app.config.setdefault('PERMANENT_SESSION_LIFETIME', timedelta(days=30))
    app.secret_key = app.config['SECRET_KEY'] # Получаем из конфигурации


def login(user_repository, username, password): # Добавлено внедрение зависимостей
    try:
        user = user_repository.get_by_username(username)
        if user is None:
            raise UserNotFoundError("User not found")
        if not check_password_hash(user.password, password):
            raise IncorrectPasswordError("Incorrect password")
        create_session(user.id)
        return make_response(message="Login successful"), 200
    except UserNotFoundError as e:
        return make_response(message=str(e), error='user_not_found'), 404
    except IncorrectPasswordError as e:
        return make_response(message=str(e), error='incorrect_password'), 401
    except SQLAlchemyError as e: #Более специфичная обработка ошибок SQLAlchemy
        return make_response(message=f"Database error: {e}", error='database_error'), 500
    except Exception as e:
        return make_response(message=f"An unexpected error occurred: {e}", error='server_error'), 500


def create_session(user_id):
    session['user_id'] = user_id
    session.permanent = True

def get_user_id():
    return session.get('user_id')

def logout():
    session.clear()
    return make_response(message="Logout successful"), 200

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_id()
        if not user_id:
            return make_response(message='Авторизация необходима', error='auth_required'), 401
        return f(*args, **kwargs)
    return decorated_function