from core.database.models import Message, db
from sqlalchemy import desc


class MessageRepository:
    def create(self, chat_id, user_id, text):
        new_message = Message(chat_id=chat_id, user_id=user_id, text=text, timestamp=db.func.now())
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def get_by_id(self, message_id):
        return Message.query.get(message_id)

    def get_all_by_chat_id(self, chat_id):
        return Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
