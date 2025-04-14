from flask import jsonify
from typing import Optional, Dict, Any


def make_response(
    message: str = "", data: Optional[Dict[str, Any]] = None, errors: Optional[Dict[str, Any]] = None, status_code: int = 200
):
    response = {"message": message}
    if data:
        response["data"] = data
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code


def success_response(data: Optional[Dict[str, Any]] = None, message: str = "Success") -> tuple[jsonify, int]:
    return make_response(message=message, data=data)


def error_response(message: str, errors: Optional[Dict[str, Any]] = None, status_code: int = 400) -> tuple[jsonify, int]:
    return make_response(message=message, errors=errors, status_code=status_code)


def not_found_response(message: str = "Resource not found") -> tuple[jsonify, int]:
    return error_response(message, status_code=404)


def unauthorized_response(message: str = "Unauthorized") -> tuple[jsonify, int]:
    return error_response(message, status_code=401)


def forbidden_response(message: str = "Forbidden") -> tuple[jsonify, int]:
    return error_response(message, status_code=403)


def server_error_response(message: str = "Server error") -> tuple[jsonify, int]:
    return error_response(message, status_code=500)


def validation_error_response(message: str = "Validation error", errors: Optional[Dict[str, Any]] = None) -> tuple[jsonify, int]:
    return error_response(message, errors, status_code=400)