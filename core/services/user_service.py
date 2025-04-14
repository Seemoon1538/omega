import re
from sqlite3 import IntegrityError
from email_validator import validate_email, EmailNotValidError
from core.database.repository.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, request, session, current_app
from itsdangerous import URLSafeTimedSerializer
from core.exceptions import (
    InvalidCredentialsError, 
    DatabaseError, 
    UserAlreadyExistsError, 
    WeakPasswordError, 
    InvalidEmailError, 
    InvalidUsernameError
)
from core.database.models import User
import logging
from functools import wraps
from core.database import db
from core.blueprints.user import SQLAlchemyError, user_blueprint
from core.security.auth_service import login_required

class UserService:
    def __init__(self, db):
        self.db = db
        self.repository = UserRepository(db)

    def create_session(self, user_id):
        session['user_id'] = user_id
        session.permanent = True

    def get_user_id(self):
        return session.get('user_id')

    def generate_secure_token(self, user_id, salt="user-confirmation"):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(user_id, salt=salt)

    def check_auth(self, user_id):
        return self.repository.get_by_id(user_id)

    def role_required(self, role):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user = self.check_auth(self.get_user_id())
                if not user or user.role != role:
                    return {"message": "Доступ запрещен", "error": "forbidden"}, 403
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def register(self, username, password, email):
        try:
            # Валидация имени пользователя
            if not re.match(r"^[a-zA-Z0-9._-]+$", username):
                raise InvalidUsernameError("Недопустимый формат имени пользователя")

            # Валидация email
            try:
                valid = validate_email(email)
                email = valid.normalized
            except EmailNotValidError:
                raise InvalidEmailError("Недействительный email")

            # Валидация пароля
            if (len(password) < 8 or 
                not re.search("[A-Z]", password) or 
                not re.search("[a-z]", password) or 
                not re.search("[0-9]", password)):
                raise WeakPasswordError("Слабый пароль")

            hashed_password = generate_password_hash(password)
            new_user = self.repository.create(username, hashed_password, email)
            return new_user

        except (UserAlreadyExistsError, IntegrityError) as e:
            logging.error(f"Ошибка базы данных при регистрации: {e}")
            raise UserAlreadyExistsError("Пользователь уже существует")
        except (InvalidUsernameError, InvalidEmailError, WeakPasswordError) as e:
            logging.warning(f"Ошибка валидации при регистрации: {e}")
            raise
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при регистрации: {e}")
            raise DatabaseError("Ошибка сервера при регистрации")
        
user_service = UserService(db)
user_repository = user_service.repository
create_session = user_service.create_session
get_user_id = user_service.get_user_id
generate_secure_token = user_service.generate_secure_token
check_auth = user_service.check_auth
role_required = user_service.role_required

@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username, password, email = data.get('username'), data.get('password'), data.get('email')

    if not all([username, password, email]):
        return make_response(message='Заполните все поля', error='missing_fields'), 400

    try:
        email = validate_email(email).normalized
    except EmailNotValidError:
        return make_response(message='Неверный формат email', error='invalid_email'), 400

    if not re.match(r"^[a-zA-Z0-9._-]+$", username):
        return make_response(message='Неверный формат имени пользователя', error='invalid_username'), 400

    if len(password) < 8 or not re.search(r"[A-Z].*[a-z]|[a-z].*[A-Z]", password) or not re.search(r"[0-9]", password):
        return make_response(message='Пароль должен быть >= 8 символов с A-Z, a-z, 0-9', error='weak_password'), 400

    if user_repository.get_by_username(username) or user_repository.get_by_email(email):
        return make_response(message='Имя или email заняты', error='user_exists'), 409

    try:
        hashed_password = generate_password_hash(password)
        new_user = user_repository.create(username, hashed_password, email)
        return make_response(message='Пользователь создан', data={'user_id': new_user.id}), 201
    except (UserAlreadyExistsError, SQLAlchemyError) as e:
        logging.exception(f"DB error: {e}")
        return make_response(message='Ошибка базы данных', error='db_error'), 500
    except Exception as e:
        logging.exception(f"Server error: {e}")
        return make_response(message='Ошибка сервера', error='server_error'), 500

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')

    if not all([username, password]):
        return make_response(message='Введите имя и пароль', error='missing_fields'), 400

    try:
        user = user_repository.get_by_username(username)
        if not user or not check_password_hash(user.password, password):
            raise InvalidCredentialsError('Неверный логин или пароль')
        create_session(user.id)
        return make_response(message='Успешный вход'), 200
    except InvalidCredentialsError as e:
        return make_response(message=str(e), error='invalid_credentials'), 401
    except SQLAlchemyError as e:
        logging.exception(f"DB error: {e}")
        return make_response(message='Ошибка базы данных', error='db_error'), 500
    except Exception as e:
        logging.exception(f"Server error: {e}")
        return make_response(message='Ошибка сервера', error='server_error'), 500

@user_blueprint.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return make_response(message='Успешный выход'), 200 
@user_blueprint.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = user_repository.get_by_id(get_user_id())
    if not user:
        return make_response(message='Пользователь не найден', error='user_not_found'), 404
    return make_response(data={'username': user.username, 'email': user.email, 'balance': user.balance}), 200

@user_blueprint.route('/secret_key', methods=['GET'])
@login_required
@role_required('admin')
def get_secret_key():
    user = check_auth(get_user_id())
    if not user:
        return make_response(message='Пользователь не найден', error='user_not_found'), 404
    return make_response(data={'secret_key': user.secret_key}), 200

@user_blueprint.route('/generate_secret_key', methods=['POST'])
@login_required
def generate_secret_key():
    user_id = get_user_id()
    user = check_auth(user_id)
    if not user:
        return make_response(message='Пользователь не найден', error='user_not_found'), 404

    try:
        new_secret_key = generate_secure_token()
        user.secret_key = new_secret_key
        user_repository.update(user)
        return make_response(message='Секретный ключ сгенерирован', data={'secret_key': new_secret_key}), 200
    except Exception as e:
        logging.exception(f"Server error: {e}")
        return make_response(message='Ошибка сервера', error='server_error'), 500
# Использование в app.py:
# from core.database import db
# user_service = UserService(db)