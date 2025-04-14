from core.database.models import Notification
from core.database import db
from core.utils.email_utils import send_email
from datetime import datetime

class NotificationService:
    def create_notification(self, text):
        notification = Notification(text=text, created_at=datetime.utcnow())
        db.session.add(notification)
        db.session.commit()
        return notification

    def get_notifications(self):
      user = user.query.get(1) # Replace with current user retrieval
      return Notification.query.filter_by(user_id=user.id).all()

    def mark_as_read(self, notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()

    def send_notification_email(self, user, subject, message):
        send_email(user.email, subject, message)