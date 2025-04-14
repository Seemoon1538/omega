from core.security.authorization import principals # Импорт principals
from core.security.authorization import init_authorization
from .auth_service import login_required


def init_app(app):
    init_authorization(app)