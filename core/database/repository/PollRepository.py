from core.database.models import Poll, db

class PollRepository:
    def create(self, question):
        new_poll = Poll(question=question, timestamp=db.func.now())
        db.session.add(new_poll)
        db.session.commit()
        return new_poll

    def get_by_id(self, poll_id):
        return Poll.query.get(poll_id)

    def get_all(self):
        return Poll.query.all()