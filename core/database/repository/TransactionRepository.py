from core.database.models import Transaction
from core.database import db
from sqlalchemy import desc


class TransactionRepository:
    def create(self, user_id, type, amount, description=None):
        new_transaction = Transaction(user_id=user_id, type=type, amount=amount, description=description, timestamp=db.func.now())
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction

    def get_by_id(self, transaction_id):
        return Transaction.query.get(transaction_id)

    def get_all_by_user_id(self, user_id, limit=100, offset=0):
        return Transaction.query.filter_by(user_id=user_id).order_by(desc(Transaction.timestamp)).limit(limit).offset(offset).all()

    def get_all(self, limit=100, offset=0):
        return Transaction.query.order_by(desc(Transaction.timestamp)).limit(limit).offset(offset).all()

    def get_last_transaction_for_user(self, user_id):
        return Transaction.query.filter_by(user_id=user_id).order_by(desc(Transaction.timestamp)).first()
    
    def __init__(self, db):
           self.db = db
