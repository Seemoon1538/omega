from core.database.models import Chat, db
from sqlalchemy.exc import IntegrityError


class ChatRepository:
    def create(self, user_ids):
        try:
            new_chat = Chat(user_ids=user_ids)
            db.session.add(new_chat)
            db.session.commit()
            return new_chat
        except IntegrityError:
            db.session.rollback()
            return None

    def get_by_id(self, chat_id):
        return Chat.query.get(chat_id)

    def get_all_by_user_id(self, user_id):
        return Chat.query.filter(Chat.user_ids.contains(user_id)).all()
