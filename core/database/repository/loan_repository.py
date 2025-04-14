from core.database.models import Loan, db

class LoanRepository:
    def __init__(self):
        self.db = db

    def create(self, user_id, amount, interest_rate, term, status):
        new_loan = Loan(
            user_id=user_id,
            amount=amount,
            interest_rate=interest_rate,
            term=term,
            status=status,
            timestamp=db.func.now()
        )
        db.session.add(new_loan)
        db.session.commit()
        return new_loan

    def get_by_id(self, loan_id):
        return Loan.query.get(loan_id)

    def get_all_by_user_id(self, user_id):
        return Loan.query.filter_by(user_id=user_id).all()

    def update(self, loan):
        db.session.commit()
        return loan