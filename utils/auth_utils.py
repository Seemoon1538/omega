from functools import wraps
from flask import request, jsonify, session
from core.database.models import User
from core.utils.response import make_response

def check_auth(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(message='Пользователь не найден', error='user_not_found'), 404
    return user

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return make_response(message='Авторизация необходима', error='auth_required'), 401
        user = check_auth(user_id)
        if not user:
            return user
        return fn(user, *args, **kwargs)
    return wrapper

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                return make_response(message='Авторизация необходима', error='auth_required'), 401
            user = check_auth(user_id)
            if not user or user.role != role:
                return make_response(message=f'У вас нет прав {role}', error=f'permission_denied_{role}'), 403
            return fn(user, *args, **kwargs)
        return wrapper
    return decorator