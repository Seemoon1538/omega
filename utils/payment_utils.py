import os
import requests
from core.exceptions import PaymentError
from dotenv import load_dotenv

load_dotenv() #Загружаем переменные окружения из .env файла

PAYMENT_GATEWAY_API_KEY = os.environ.get('PAYMENT_GATEWAY_API_KEY')
PAYMENT_GATEWAY_API_URL = os.environ.get('PAYMENT_GATEWAY_API_URL')


if not PAYMENT_GATEWAY_API_KEY or not PAYMENT_GATEWAY_API_URL:
    raise ValueError("PAYMENT_GATEWAY_API_KEY and PAYMENT_GATEWAY_API_URL environment variables must be set.")


def process_payment(amount, currency, description, metadata=None):
    """Обрабатывает платеж через платежный шлюз."""
    headers = {
        'Authorization': f'Bearer {PAYMENT_GATEWAY_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'amount': amount,
        'currency': currency,
        'description': description,
        'metadata': metadata or {},
    }
    try:
        response = requests.post(PAYMENT_GATEWAY_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        payment_data = response.json()
        return payment_data['id'] #Или другое значение, идентифицирующее платеж
    except requests.exceptions.RequestException as e:
        raise PaymentError(f"Payment processing failed: {e}")


def get_payment_status(payment_id):
    """Получает статус платежа."""
    headers = {
        'Authorization': f'Bearer {PAYMENT_GATEWAY_API_KEY}',
        'Content-Type': 'application/json',
    }
    url = f"{PAYMENT_GATEWAY_API_URL}/{payment_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        payment_data = response.json()
        return payment_data['status']
    except requests.exceptions.RequestException as e:
        raise PaymentError(f"Failed to get payment status: {e}")