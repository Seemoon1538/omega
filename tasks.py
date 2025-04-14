from celery import Celery
from backend.core.database.models import Notification
from backend.core.database.repository.user_repository import User
from core.services.notification_service import NotificationService
from core.utils.email_utils import send_email
from core.database import db
from flask import current_app

celery = Celery(__name__, broker='amqp://guest:guest@localhost:5672//') # Replace with your broker URL

notification_service = NotificationService()

@celery.task()
def send_email_task(user_id, subject, message):
    with current_app.app_context():
        try:
            user = User.query.get(user_id)
            if user:
                send_email(user.email, subject, message)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")

@celery.task()
def send_notifications_task(user_id, notification_ids):
    with current_app.app_context():
        try:
            user = User.query.get(user_id)
            if user:
                for notification_id in notification_ids:
                    notification = Notification.query.get(notification_id)
                    if notification:
                        #You can add logic to send notification through different channels here
                        send_email_task.delay(user_id, "New Notification", notification.text)


        except Exception as e:
            print(f"Ошибка отправки уведомлений: {e}")