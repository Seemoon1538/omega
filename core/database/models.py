from core.database import db # импортируем db из flask_sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    secret_key = db.Column(db.String(120), nullable=False) # хранение secret_key в базе данных - небезопасно!
    balance = db.Column(db.Float, default=0.0)
    transactions = relationship("Transaction", backref="user", lazy=True)
    loans = relationship("Loan", backref="user", lazy=True)
    investments = relationship("Investment", backref="user", lazy=True)
    notifications = relationship("Notification", backref="user", lazy=True)
    votes = relationship("Vote", backref="user", lazy=True)
    messages = relationship("Message", backref="user", lazy=True)
    chats = relationship("Chat", secondary="chat_user", backref="users", lazy=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    description = db.Column(db.Text)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, ForeignKey('project.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    investments = relationship("Investment", backref="project", lazy=True)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    is_read = db.Column(db.Boolean, default=False)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    options = relationship("PollOption", backref="poll", lazy=True)


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    votes = relationship("Vote", backref="option", lazy=True)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    poll_id = db.Column(db.Integer, ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, ForeignKey('poll_option.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_ids = db.Column(db.ARRAY(db.Integer), nullable=False)
    messages = relationship("Message", backref="chat", lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())

class ChatUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, ForeignKey('chat.id'), nullable=False)