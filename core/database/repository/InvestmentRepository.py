from core.database.models import Investment, db

class InvestmentRepository:
    def create(self, user_id, project_id, amount):
        new_investment = Investment(user_id=user_id, project_id=project_id, amount=amount, timestamp=db.func.now())
        db.session.add(new_investment)
        db.session.commit()
        return new_investment

    def get_by_id(self, investment_id):
        return Investment.query.get(investment_id)

    def get_all_by_user_id(self, user_id):
        return Investment.query.filter_by(user_id=user_id).all()

    def get_all_by_project_id(self, project_id):
        return Investment.query.filter_by(project_id=project_id).all()

    def get_sum_by_project_id(self, project_id):
        return db.session.query(db.func.sum(Investment.amount)).filter_by(project_id=project_id).scalar()