from core.database.models import Notification, db

class NotificationRepository:
    def create(self, user_id, message):
        new_notification = Notification(user_id=user_id, message=message, timestamp=db.func.now(), is_read=False)
        db.session.add(new_notification)
        db.session.commit()
        return new_notification

    def get_by_id(self, notification_id):
        return Notification.query.get(notification_id)

    def get_unread_by_user_id(self, user_id):
        return Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.timestamp.desc()).all()

    def update(self, notification):
        db.session.commit()
        return notification

    def mark_as_read(self, notification_id):
        notification = self.get_by_id(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
            return notification
        return None
