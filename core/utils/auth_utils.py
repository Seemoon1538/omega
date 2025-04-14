from functools import wraps
from flask import request, jsonify
from core.exceptions import AuthenticationError
from backend.core.security import auth_service
from flask import g


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationError("Authorization header missing")
        try:
            token = auth_header.split(" ")[1]
            user_id = auth_service.verify_jwt_token(token)
            g.user = user_repository.get_by_id(user_id)
            return f(*args, **kwargs)
        except Exception as e:
            raise AuthenticationError(str(e))
    return decorated


from backend.core.database.repository import user_repository

user_repository = user_repository()