from flask import Blueprint, request
from flask_login import login_required, current_user
from core.database.repository.TransactionRepository import TransactionRepository
from backend.core.database.repository.user_repository import UserRepository
from core.database import db
from core.exceptions import AuthenticationError, AuthorizationError, DatabaseError, InsufficientFundsError
from core.utils import is_valid_amount
from core.utils.response import make_response


transaction_blueprint = Blueprint('transactions', __name__, url_prefix='/transactions')

transaction_repository = TransactionRepository(db)
user_repository = UserRepository(db)

@transaction_blueprint.route('/', methods=['POST'])
@login_required
def create_transaction():
    try:
        data = request.get_json()
        recipient_username = data.get('recipient_username')
        amount = data.get('amount')
        description = data.get('description', '')

        if not all([recipient_username, amount]):
            return make_response(message='Укажите получателя и сумму', error='missing_fields'), 400

        if not is_valid_amount(amount):
            return make_response(message='Неверная сумма', error='invalid_amount'), 400

        sender = current_user
        recipient = user_repository.get_by_username(recipient_username)

        if not recipient:
            return make_response(message='Получатель не найден', error='recipient_not_found'), 404

        if sender.balance < float(amount):
            raise InsufficientFundsError("Недостаточно средств")

        sender.balance -= float(amount)
        recipient.balance += float(amount)
        
        transaction = transaction_repository.create(sender.id, 'transfer', float(amount), description)
        if not transaction:
            raise DatabaseError("Ошибка создания транзакции")
        return make_response(message='Транзакция создана', data={'transaction_id': transaction.id}), 201

    except (DatabaseError, InsufficientFundsError) as e:
        return make_response(message=str(e), error=type(e).__name__.lower()), 500
    except Exception as e:
        return make_response(message=f"Unexpected error: {e}", error='server_error'), 500


@transaction_blueprint.route('/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    try:
        transaction = transaction_repository.get_by_id(transaction_id)
        if not transaction:
            return make_response(message='Транзакция не найдена', error='transaction_not_found'), 404

        sender = user_repository.get_by_id(transaction.user_id)
        if not sender:
            return make_response(message='Пользователь не найден', error='sender_not_found'), 404

        return make_response(data={'transaction': transaction.to_dict(), 'sender': sender.username}), 200
    except Exception as e:
        return make_response(message=f"Unexpected error: {e}", error='server_error'), 500



@transaction_blueprint.route('/history', methods=['GET'])
@login_required
def get_transactions_history():
    try:
        user_id = current_user.id
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 100))
        transactions = transaction_repository.get_all_by_user_id(user_id, limit, (page - 1) * limit)
        return make_response(data=[transaction.to_dict() for transaction in transactions]), 200
    except Exception as e:
        return make_response(message=f"Unexpected error: {e}", error='server_error'), 500