from flask import Blueprint, request, jsonify
from core.services.transaction_service import TransactionService
from core.utils.auth_utils import login_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError


transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')
transaction_service = TransactionService()

class TransactionSchema(Schema):
    type = fields.Str(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True)
    details = fields.Str()


@transactions_bp.route('/', methods=['GET'])
@login_required
def get_transactions():
    try:
        transactions = transaction_service.get_transactions()
        return make_response(transactions=[t.to_dict() for t in transactions]), 200
    except Exception as e:
        return make_response(message=str(e)), 500


@transactions_bp.route('/deposit', methods=['POST'])
@login_required
def create_deposit():
    try:
        data = TransactionSchema().load(request.json)
        data['type'] = 'deposit'
        transaction = transaction_service.create_transaction(**data)
        return make_response(transaction=transaction.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500


@transactions_bp.route('/withdrawal', methods=['POST'])
@login_required
def create_withdrawal():
    try:
        data = TransactionSchema().load(request.json)
        data['type'] = 'withdrawal'
        transaction = transaction_service.create_transaction(**data)
        return make_response(transaction=transaction.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500