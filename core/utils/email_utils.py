from flask_mail import Message
from core.database import db
from core.exceptions import OmegaException
from flask import current_app


class EmailSendingError(OmegaException):
    """Исключение, возникающее при ошибках отправки email."""
    status_code = 500


def send_email(subject, recipients, html_body):
    """Отправляет email сообщение."""
    msg = Message(subject, recipients=recipients, html=html_body)
    try:
        with current_app.app_context():
          mail = current_app.mail
          mail.send(msg)
    except Exception as e:
        db.session.rollback()
        raise EmailSendingError(f"Failed to send email: {e}")