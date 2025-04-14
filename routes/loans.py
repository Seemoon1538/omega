from flask import Blueprint, request, jsonify
from core.services.loan_service import LoanService
from core.utils.auth_utils import login_required, investor_required
from core.utils.response import make_response
from core.utils.validation import validate_amount, validate_required
from marshmallow import Schema, fields, ValidationError

loans_bp = Blueprint('loans', __name__, url_prefix='/api/loans')
loan_service = LoanService()

class LoanRequestSchema(Schema):
    amount = fields.Float(required=True)
    purpose = fields.Str(required=True)

class VoteSchema(Schema):
    vote = fields.Str(required=True, validate=lambda n: n in ['approve', 'reject'])

@loans_bp.route('/request', methods=['POST'])
@login_required
def create_loan_request():
    try:
        data = LoanRequestSchema().load(request.json)
        errors = validate_amount(data['amount'], 0, None) + validate_required(data['purpose'])
        if errors:
            raise ValidationError(errors)
        loan = loan_service.create_loan_request(data['amount'], data['purpose'])
        return make_response(loan=loan.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@loans_bp.route('/<int:loan_id>/vote', methods=['POST'])
@investor_required
def vote_on_loan(loan_id):
    try:
        data = VoteSchema().load(request.json)
        loan_service.vote_on_loan(loan_id, data['vote'])
        return make_response(message='Голос учтен'), 200
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@loans_bp.route('/<int:loan_id>', methods=['GET'])
@login_required
def get_loan(loan_id):
    try:
        loan = loan_service.get_loan(loan_id)
        if not loan:
            return make_response(message='Заявка на кредит не найдена'), 404
        return make_response(loan=loan.to_dict()), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@loans_bp.route('/', methods=['GET'])
@login_required
def get_user_loans():
    loans = loan_service.get_user_loans()
    return make_response(loans=[loan.to_dict() for loan in loans]), 200