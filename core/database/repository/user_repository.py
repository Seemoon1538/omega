from typing import Optional  # Используем Optional для secret_key
from core.database.models import User
from core.database import db
from sqlalchemy.exc import IntegrityError
from core.exceptions import UserAlreadyExistsError, DatabaseError

class UserRepository:
    def __init__(self, db):  # Исправлено на __init__
        self.db = db

    def get_user(self, user_id: int) -> Optional[User]:  # Убран дубликат, добавлены аннотации
        return self.db.session.query(User).get(user_id)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.session.query(User).get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.session.query(User).filter_by(username=username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.session.query(User).filter_by(email=email).first()

    def create(self, username: str, password: str, email: str, secret_key: Optional[str] = None) -> User:
        try:
            new_user = User(
                username=username,
                password=password,
                email=email,
                secret_key=secret_key
            )
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except IntegrityError:
            self.db.session.rollback()
            raise UserAlreadyExistsError("Пользователь с таким именем или email уже существует")
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Ошибка базы данных при создании пользователя: {e}") from e

    def update(self, user: User) -> User:
        try:
            self.db.session.add(user)
            self.db.session.commit()
            return user
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Ошибка базы данных при обновлении пользователя: {e}") from e

    def delete(self, user: User) -> bool:
        try:
            self.db.session.delete(user)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            raise DatabaseError(f"Ошибка базы данных при удалении пользователя: {e}") from e