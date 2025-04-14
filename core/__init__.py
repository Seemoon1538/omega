from core.security import init_app as init_security_app
from core.utils import configure_logging

def init_app(app):
    init_security_app(app)
    configure_logging(app)