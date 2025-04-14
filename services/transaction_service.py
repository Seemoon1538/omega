from core.database.models import User, Transaction, Deposit, Withdrawal
from core.database import db
from datetime import datetime

class TransactionService:
    def create_transaction(self, type, amount, currency, details=None):
        user = User.query.get(1) # Replace with current user retrieval
        transaction = Transaction(user_id=user.id, type=type, amount=amount, currency=currency, details=details, created_at=datetime.utcnow())
        db.session.add(transaction)

        if type == 'deposit':
            deposit = Deposit(transaction_id=transaction.id, payment_method='example', payment_id='example_id') #replace with actual payment data
            db.session.add(deposit)
        elif type == 'withdrawal':
            withdrawal = Withdrawal(transaction_id=transaction.id, destination_address=details)
            db.session.add(withdrawal)

        db.session.commit()
        return transaction

    def get_transactions(self):
        user = User.query.get(1) # Replace with current user retrieval
        return Transaction.query.filter_by(user_id=user.id).all()