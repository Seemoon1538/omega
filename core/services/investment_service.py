from flask import request, jsonify
from flask_login import login_required
from core.database.repository.user_repository import UserRepository
from core.database.repository.ProjectRepository import  ProjectRepository
from core.database.repository.InvestmentRepository import InvestmentRepository
from core.security import auth_service
from core.services import investment_blueprint
from core.exceptions import AuthenticationError, AuthorizationError
from core.utils import is_valid_amount


investment_repository = InvestmentRepository()
user_repository = UserRepository()
project_repository = ProjectRepository()


@investment_blueprint.route('/', methods=['POST'])
@login_required
def create_investment():
    data = request.get_json()
    project_id = data.get('project_id')
    amount = data.get('amount')

    if not project_id or not amount:
        return jsonify({'error': 'Missing project_id or amount'}), 400

    if not is_valid_amount(amount):
        return jsonify({'error': 'Invalid amount'}), 400

    user_id = auth_service.get_jwt_identity()
    user = user_repository.get_by_id(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    project = project_repository.get_by_id(project_id)
    if project is None:
        return jsonify({'error': 'Project not found'}), 404

    if user.balance < float(amount):
        return jsonify({'error': 'Insufficient balance'}), 400

    user.balance -= float(amount)
    project.current_amount += float(amount)

    new_investment = investment_repository.create(user_id, project_id, float(amount))
    if new_investment is None:
        return jsonify({'error': 'Failed to create investment'}), 500

    return jsonify({'message': 'Investment created successfully', 'investment_id': new_investment.id}), 201



@investment_blueprint.route('/<int:investment_id>', methods=['GET'])
@login_required
def get_investment(investment_id):
    investment = investment_repository.get_by_id(investment_id)
    if investment is None:
        return jsonify({'error': 'Investment not found'}), 404
    return jsonify(investment.to_dict()), 200


@investment_blueprint.route('/history', methods=['GET'])
@login_required
def get_investments_history():
    user_id = auth_service.get_jwt_identity()
    investments = investment_repository.get_all_by_user_id(user_id)
    return jsonify([investment.to_dict() for investment in investments]), 200
