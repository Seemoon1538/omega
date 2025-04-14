from flask import request, jsonify
from flask_login import login_required
from core.database.repository.user_repository import UserRepository, db
from core.database.repository.MessageRepository import  MessageRepository
from core.database.repository.ChatRepository import ChatRepository
from core.security import auth_service
from core.blueprints.chat import chat_blueprint
from core.exceptions import AuthenticationError, AuthorizationError, ValidationError
from core.utils import is_valid_amount


chat_repository = ChatRepository()
message_repository = MessageRepository()
user_repository = UserRepository(db)


@chat_blueprint.route('/', methods=['POST'])
@login_required
def create_chat():
    data = request.get_json()
    user_ids = data.get('user_ids')

    if not user_ids or len(user_ids) < 2:
        return jsonify({'error': 'At least two user IDs are required'}), 400
    
    user_id = auth_service.get_jwt_identity()
    if user_id not in user_ids:
        return jsonify({'error': 'User ID must be included in user_ids'}), 400

    for user_id in user_ids:
        user = user_repository.get_by_id(user_id)
        if user is None:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404


    new_chat = chat_repository.create(user_ids)
    if new_chat is None:
        return jsonify({'error': 'Failed to create chat'}), 500
    return jsonify({'chat_id': new_chat.id}), 201



@chat_blueprint.route('/<int:chat_id>', methods=['GET'])
@login_required
def get_chat(chat_id):
    chat = chat_repository.get_by_id(chat_id)
    if chat is None:
        return jsonify({'error': 'Chat not found'}), 404

    user_id = auth_service.get_jwt_identity()
    if user_id not in chat.user_ids:
        return jsonify({'error': 'Unauthorized'}), 403
    
    messages = message_repository.get_all_by_chat_id(chat_id)

    return jsonify({'chat_id': chat.id, 'messages': [message.to_dict() for message in messages]}), 200


@chat_blueprint.route('/<int:chat_id>/messages', methods=['POST'])
@login_required
def create_message(chat_id):
    data = request.get_json()
    message_text = data.get('message')

    if not message_text:
        return jsonify({'error': 'Missing message'}), 400

    chat = chat_repository.get_by_id(chat_id)
    if chat is None:
        return jsonify({'error': 'Chat not found'}), 404
    
    user_id = auth_service.get_jwt_identity()
    if user_id not in chat.user_ids:
        return jsonify({'error': 'Unauthorized'}), 403

    new_message = message_repository.create(chat_id, user_id, message_text)
    if new_message is None:
        return jsonify({'error': 'Failed to create message'}), 500

    return jsonify({'message_id':new_message.id}), 201