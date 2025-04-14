from flask import Blueprint, g, jsonify, current_app
from core.database.repository.user_repository import UserRepository
from core.exceptions import AuthorizationError
from core.security.auth_service import login_required
from flask_login import AnonymousUserMixin, current_user
from core.utils.response import make_response
from core.database import db


principals = {
    'admin': ['admin', 'user'],
    'user': ['user']
}


bp = Blueprint('admin', __name__, url_prefix='/admin')


class Anonymous(AnonymousUserMixin):
    pass

def init_authorization(app):
    with app.app_context(): # Инициализация UserRepository в контексте приложения
        user_repository = UserRepository(db)


def requires_role(role):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = current_user
            if not user or not user.is_authenticated or role not in user.roles:
                return make_response(message=f'Доступ запрещен: Требуется роль {role}', error='authorization_error'), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('')
@login_required
@requires_role('admin')
def admin_route():
    return make_response(message='Админский маршрут')