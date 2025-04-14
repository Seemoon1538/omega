from flask import request, jsonify
from flask_login import current_user
from core.database.repository.loan_repository import LoanRepository
from core.database.repository.user_repository import UserRepository
from core.security import requires_role, login_required
from core.blueprints.loan import loan_blueprint  # Новый импорт
from core.utils import is_valid_amount
from core.database import db

loan_repository = LoanRepository()
user_repository = UserRepository(db)


@loan_blueprint.route('/', methods=['POST'])
@login_required
def create_loan_request():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        amount = data.get('amount')
        interest_rate = data.get('interest_rate')
        term = data.get('term')  # Срок в месяцах

        if not all([amount, interest_rate, term]):
            return jsonify({'error': 'Missing required fields'}), 400

        if not all(is_valid_amount(x) for x in [amount, interest_rate, term]):
            return jsonify({'error': 'Invalid numeric values'}), 400

        user_id = current_user.id  # Используем current_user от flask_login
        user = user_repository.get_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_loan = loan_repository.create(
            user_id=user_id,
            amount=float(amount),
            interest_rate=float(interest_rate),
            term=int(term),
            status='pending'
        )
        
        if not new_loan:
            return jsonify({'error': 'Failed to create loan request'}), 500

        return jsonify({
            'message': 'Loan request created successfully',
            'loan_id': new_loan.id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_blueprint.route('/<int:loan_id>', methods=['GET'])
@login_required
def get_loan(loan_id):
    try:
        loan = loan_repository.get_by_id(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_blueprint.route('/<int:loan_id>/approve', methods=['POST'])
@login_required
@requires_role('admin')
def approve_loan(loan_id):
    try:
        loan = loan_repository.get_by_id(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
            
        loan.status = 'approved'
        loan_repository.update(loan)
        return jsonify({'message': 'Loan approved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_blueprint.route('/<int:loan_id>/reject', methods=['POST'])
@login_required
@requires_role('admin')
def reject_loan(loan_id):
    try:
        loan = loan_repository.get_by_id(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
            
        loan.status = 'rejected'
        loan_repository.update(loan)
        return jsonify({'message': 'Loan rejected successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_blueprint.route('/history', methods=['GET'])
@login_required
def get_loans_history():
    try:
        user_id = current_user.id
        loans = loan_repository.get_all_by_user_id(user_id)
        return jsonify([loan.to_dict() for loan in loans]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500