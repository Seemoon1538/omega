from flask import Blueprint, request, jsonify
from core.services.investment_service import InvestmentService
from core.utils.logging import login_required
from core.utils.response import make_response
from core.utils.validation import validate_amount, validate_required
from marshmallow import Schema, fields, ValidationError

investments_bp = Blueprint('investments', __name__, url_prefix='/api/investments')
investment_service = InvestmentService()

class InvestmentSchema(Schema):
    level_id = fields.Int(required=True)
    amount = fields.Float(required=True)

@investments_bp.route('/', methods=['POST'])
@login_required
def create_investment():
    try:
        data = InvestmentSchema().load(request.json)
        errors = validate_required(data['level_id']) + validate_amount(data['amount'], 0, None)
        if errors:
            raise ValidationError(errors)
        investment = investment_service.create_investment(data['level_id'], data['amount'])
        return make_response(investment=investment.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@investments_bp.route('/levels', methods=['GET'])
def get_investment_levels():
    try:
        levels = investment_service.get_investment_levels()
        return make_response(levels=[level.to_dict() for level in levels]), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@investments_bp.route('/<int:investment_id>', methods=['GET'])
@login_required
def get_investment(investment_id):
    try:
        investment = investment_service.get_investment(investment_id)
        if not investment:
            return make_response(message='Инвестиция не найдена'), 404
        return make_response(investment=investment.to_dict()), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@investments_bp.route('/history', methods=['GET'])
@login_required
def get_investment_history():
    try:
        investments = investment_service.get_investment_history()
        return make_response(investments=[inv.to_dict() for inv in investments]), 200
    except Exception as e:
        return make_response(message=str(e)), 500