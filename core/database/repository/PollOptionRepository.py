from core.database.models import PollOption, db

class PollOptionRepository:
    def create(self, poll_id, text):
        new_option = PollOption(poll_id=poll_id, text=text)
        db.session.add(new_option)
        db.session.commit()
        return new_option

    def get_by_id(self, option_id):
        return PollOption.query.get(option_id)

    def get_all_by_poll_id(self, poll_id):
        return PollOption.query.filter_by(poll_id=poll_id).all()