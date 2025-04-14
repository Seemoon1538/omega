from flask import Blueprint, request, jsonify
from core.services.chat_service import ChatService
from core.utils.auth_utils import login_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError

chats_bp = Blueprint('chats', __name__, url_prefix='/api/chats')
chat_service = ChatService()

class ChatSchema(Schema):
    recipient_id = fields.Int(required=True)

class MessageSchema(Schema):
    text = fields.Str(required=True)

@chats_bp.route('/', methods=['POST'])
@login_required
def create_chat():
    try:
        data = ChatSchema().load(request.json)
        chat = chat_service.create_chat(data['recipient_id'])
        return make_response(chat=chat.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@chats_bp.route('/<int:chat_id>/messages', methods=['GET'])
@login_required
def get_chat_messages(chat_id):
    try:
        messages = chat_service.get_chat_messages(chat_id)
        return make_response(messages=[m.to_dict() for m in messages]), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@chats_bp.route('/<int:chat_id>/messages', methods=['POST'])
@login_required
def send_message(chat_id):
    try:
        data = MessageSchema().load(request.json)
        message = chat_service.send_message(chat_id, data['text'])
        return make_response(message=message.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500