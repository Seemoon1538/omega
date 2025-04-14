from flask import Blueprint, request, jsonify
from core.services.message_service import MessageService
from core.utils.auth_utils import login_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError

messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages') #Renamed to avoid conflict
message_service = MessageService()

class MessageSchema(Schema):
    text = fields.Str(required=True)

@messages_bp.route('/<int:chat_id>', methods=['POST'])
@login_required
def send_message(chat_id):
    try:
        data = MessageSchema().load(request.json)
        message = message_service.send_message(chat_id, data['text'])
        return make_response(message=message.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@messages_bp.route('/<int:chat_id>', methods=['GET'])
@login_required
def get_messages(chat_id):
    try:
        messages = message_service.get_messages(chat_id)
        return make_response(messages=[msg.to_dict() for msg in messages]), 200
    except Exception as e:
        return make_response(message=str(e)), 500
