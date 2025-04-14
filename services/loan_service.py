from core.database.models import User, Loan, Vote
from core.database import db
from random import sample

class LoanService:
    def create_loan_request(self, amount, purpose):
        user = User.query.get(1) # Replace with current user retrieval
        loan = Loan(borrower_id=user.id, amount=amount, purpose=purpose)
        db.session.add(loan)
        db.session.commit()
        return loan

    def vote_on_loan(self, loan_id, vote):
        user = User.query.get(1) # Replace with current user retrieval
        loan = Loan.query.get(loan_id)
        if not loan:
            raise Exception("Loan not found")

        vote_exists = Vote.query.filter_by(user_id=user.id, loan_id=loan_id).first()
        if vote_exists:
            raise Exception("User already voted")

        vote_obj = Vote(user_id=user.id, loan_id=loan_id, vote=vote)
        db.session.add(vote_obj)
        db.session.commit()

        # Check if enough votes are in, and update status if necessary.
        votes_count = Vote.query.filter_by(loan_id=loan_id).count()
        if votes_count >= 10:
          positive_votes = Vote.query.filter_by(loan_id=loan_id, vote='approve').count()
          if positive_votes >= 5:
            loan.status = 'approved'
          else:
            loan.status = 'rejected'
          db.session.commit()


    def get_loan(self, loan_id):
        return Loan.query.get(loan_id)

    def get_user_loans(self):
        user = User.query.get(1) # Replace with current user retrieval
        return Loan.query.filter_by(borrower_id=user.id).all()

    def get_loan_requests(self, limit=100):
      #Get all users who are investors
      investors = User.query.filter_by(role='investor').all()
      investor_ids = [investor.id for investor in investors]
      #Get all loan requests
      loan_requests = Loan.query.filter_by(status='pending').all()
      #Sample 100 loan requests
      sampled_requests = sample(loan_requests, min(len(loan_requests), limit))
      return sampled_requests