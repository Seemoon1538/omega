
from flask import Blueprint, request, jsonify
from core.services.user_service import UserService
from core.utils.auth_utils import login_required, admin_required
from core.utils.validation import validate_email, validate_password, validate_login, validate_secret_phrase
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError


users_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    secret_phrase = fields.Str(required=True)

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = UserSchema().load(request.json)
        errors = validate_email(data['email']) + validate_password(data['password']) + validate_login(data['username']) + validate_secret_phrase(data['secret_phrase'])
        if errors:
            raise ValidationError(errors)
        user_service.create_user(data['username'], data['email'], data['password'], data['secret_phrase'])
        return make_response(message='Пользователь успешно зарегистрирован'), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500


@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = user_service.authenticate_user(data.get('username'), data.get('password'))
        if user:
            token = user_service.generate_jwt(user)
            return make_response(token=token, user=user.to_dict()), 200
        else:
            return make_response(message='Неверный логин или пароль'), 401
    except Exception as e:
        return make_response(message=str(e)), 500

@users_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return make_response(user=user_service.get_current_user().to_dict()), 200

@users_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        data = request.get_json()
        user_service.update_user(data.get('username'), data.get('email'), data.get('secret_phrase'))
        return make_response(message='Профиль успешно обновлен'), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@users_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = user_service.get_all_users()
    return make_response(users=[user.to_dict() for user in users]), 200
