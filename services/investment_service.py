from core.database.models import User, Investment, InvestmentLevel
from core.database import db

class InvestmentService:
    def create_investment(self, level_id, amount):
        user = User.query.get(1) # Replace with current user retrieval
        level = InvestmentLevel.query.get(level_id)
        if not level:
            raise Exception("Investment level not found")
        investment = Investment(investor_id=user.id, level_id=level_id, amount=amount)
        db.session.add(investment)
        db.session.commit()
        return investment

    def get_investment_levels(self):
        return InvestmentLevel.query.all()

    def get_investment(self, investment_id):
        return Investment.query.get(investment_id)

    def get_investment_history(self):
        user = User.query.get(1) # Replace with current user retrieval
        return Investment.query.filter_by(investor_id=user.id).all()