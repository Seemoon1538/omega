from core.database.models import User
from core.utils.auth_utils import generate_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import db

class UserService:
    def create_user(self, username, email, password, secret_phrase):
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password, secret_phrase=secret_phrase)
        db.session.add(user)
        db.session.commit()
        return user

    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def generate_jwt(self, user):
        return generate_jwt(user)

    def get_current_user(self):
      #This needs to be implemented based on your authentication method.
      #Example using Flask-JWT-Extended:
      # from flask_jwt_extended import get_jwt_identity
      # user_id = get_jwt_identity()
      # user = User.query.get(user_id)
      # return user
        return None

    def get_all_users(self):
        return User.query.all()

    def update_user(self, username, email, secret_phrase):
        user = self.get_current_user()
        if user:
            user.username = username
            user.email = email
            user.secret_phrase = secret_phrase
            db.session.commit()
            return user
        return None

    # Add other user-related methods as needed (e.g., user profile update, password reset)