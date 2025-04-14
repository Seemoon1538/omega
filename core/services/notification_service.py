from flask import request, jsonify
from flask_login import login_required
from backend.core.database.repository import user_repository
from backend.core.security import auth_service
from core.database.repository import NotificationRepository
from core.security import authorization # Импортируем модуль authorization
from core.services import notification_blueprint
from core.exceptions import AuthenticationError, AuthorizationError


notification_repository = NotificationRepository()
user_repository = user_repository()


@notification_blueprint.route('/', methods=['POST'])
@login_required
@authorization.requires_role('admin') # Используем authorization.requires_role
def create_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({'error': 'Missing user_id or message'}), 400

    user = user_repository.get_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    new_notification = notification_repository.create(user_id, message)
    if new_notification is None:
        return jsonify({'error': 'Failed to create notification'}), 500

    return jsonify({'message': 'Notification created successfully', 'notification_id': new_notification.id}), 201



@notification_blueprint.route('/<int:notification_id>', methods=['GET'])
@login_required
def get_notification(notification_id):
    notification = notification_repository.get_by_id(notification_id)
    if notification is None:
        return jsonify({'error': 'Notification not found'}), 404
    return jsonify(notification.to_dict()), 200


@notification_blueprint.route('/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_as_read(notification_id):
  notification = notification_repository.get_by_id(notification_id)
  if notification is None:
      return jsonify({'error': 'Notification not found'}), 404
  
  user_id = auth_service.get_jwt_identity()
  if notification.user_id != user_id:
    return jsonify({'error': 'Unauthorized'}), 403

  notification.is_read = True
  notification_repository.update(notification)
  return jsonify({'message': 'Notification marked as read'}), 200



@notification_blueprint.route('/unread', methods=['GET'])
@login_required
def get_unread_notifications():
    user_id = auth_service.get_jwt_identity()
    notifications = notification_repository.get_unread_by_user_id(user_id)
    return jsonify([notification.to_dict() for notification in notifications]), 200