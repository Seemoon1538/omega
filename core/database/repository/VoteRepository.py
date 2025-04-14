from core.database.models import Vote, db

class VoteRepository:
    def create(self, user_id, poll_id, option_id):
        new_vote = Vote(user_id=user_id, poll_id=poll_id, option_id=option_id, timestamp=db.func.now())
        db.session.add(new_vote)
        db.session.commit()
        return new_vote

    def get_by_user_id_and_poll_id(self, user_id, poll_id):
        return Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()

    def get_count_by_option_id(self, option_id):
        return Vote.query.filter_by(option_id=option_id).count()