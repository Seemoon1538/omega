from flask import Blueprint, request, jsonify
from core.services.notification_service import NotificationService
from core.utils.auth_utils import login_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')
notification_service = NotificationService()

class NotificationSchema(Schema):
    text = fields.Str(required=True)

@notifications_bp.route('/', methods=['GET'])
@login_required
def get_notifications():
    try:
        notifications = notification_service.get_notifications()
        return make_response(notifications=[n.to_dict() for n in notifications]), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@login_required
def mark_as_read(notification_id):
    try:
        notification_service.mark_as_read(notification_id)
        return make_response(message='Уведомление отмечено как прочитанное'), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@notifications_bp.route('/', methods=['POST'])
def create_notification():
    try:
        data = NotificationSchema().load(request.json)
        notification = notification_service.create_notification(data['text'])
        return make_response(notification=notification.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500