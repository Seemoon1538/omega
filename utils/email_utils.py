from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail = current_app.extensions['mail']
            mail.send(msg)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


def send_email(to, subject, html_body):
    """Отправляет электронное письмо асинхронно."""
    msg = Message(subject=subject, recipients=[to], html=html_body)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
