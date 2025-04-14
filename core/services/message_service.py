from flask import request, jsonify
from flask_login import login_required
from core.database.repository.ChatRepository import  ChatRepository
from core.database.repository.MessageRepository import MessageRepository
from core.security import auth_service
from core.blueprints.message import message_blueprint
from core.exceptions import AuthenticationError, AuthorizationError, ValidationError



message_repository = MessageRepository()
chat_repository = ChatRepository()


@message_blueprint.route('/<int:message_id>', methods=['GET'])
@login_required
def get_message(message_id):
    message = message_repository.get_by_id(message_id)
    if message is None:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify(message.to_dict()), 200


@message_blueprint.route('/<int:chat_id>', methods=['GET'])
@login_required
def get_messages_by_chat_id(chat_id):
    chat = chat_repository.get_by_id(chat_id)
    if chat is None:
        return jsonify({'error': 'Chat not found'}), 404

    user_id = auth_service.get_jwt_identity()
    if user_id not in chat.user_ids:
        return jsonify({'error': 'Unauthorized'}), 403

    messages = message_repository.get_all_by_chat_id(chat_id)
    return jsonify([message.to_dict() for message in messages]), 200