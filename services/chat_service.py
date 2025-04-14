from core.database.models import Chat, Message, User
from core.database import db
from datetime import datetime

class ChatService:
    def create_chat(self, recipient_id):
        user = User.query.get(1) # Replace with current user retrieval
        recipient = User.query.get(recipient_id)
        if not recipient:
            raise Exception("Recipient not found")

        # Check if chat already exists
        existing_chat = Chat.query.filter(
            (Chat.user1_id == user.id) & (Chat.user2_id == recipient.id) |
            (Chat.user1_id == recipient.id) & (Chat.user2_id == user.id)
        ).first()
        if existing_chat:
            return existing_chat

        chat = Chat(user1_id=user.id, user2_id=recipient_id, created_at=datetime.utcnow())
        db.session.add(chat)
        db.session.commit()
        return chat

    def get_chat_messages(self, chat_id):
        return Message.query.filter_by(chat_id=chat_id).all()

    def send_message(self, chat_id, text):
        user = User.query.get(1) # Replace with current user retrieval
        message = Message(chat_id=chat_id, user_id=user.id, text=text, created_at=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return message