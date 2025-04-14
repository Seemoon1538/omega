from functools import wraps
from flask import g, jsonify
from core.exceptions import AuthorizationError
from core.security import principals


def requires_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not principals.has_role(role):
                raise AuthorizationError(f"Access denied: Requires {role} role")
            return fn(*args, **kwargs)
        return wrapper
    return decorator