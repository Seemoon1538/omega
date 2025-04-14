from flask import Blueprint, request, jsonify
from core.services.poll_service import PollService
from core.utils.auth_utils import login_required, admin_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError

polls_bp = Blueprint('polls', __name__, url_prefix='/api/polls')
poll_service = PollService()

class PollSchema(Schema):
    question = fields.Str(required=True)
    options = fields.List(fields.Str(), required=True)

class VoteSchema(Schema):
    option = fields.Str(required=True)

@polls_bp.route('/', methods=['POST'])
@admin_required
def create_poll():
    try:
        data = PollSchema().load(request.json)
        poll = poll_service.create_poll(data['question'], data['options'])
        return make_response(poll=poll.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@polls_bp.route('/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    try:
        poll = poll_service.get_poll(poll_id)
        if not poll:
            return make_response(message='Опрос не найден'), 404
        return make_response(poll=poll.to_dict()), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@polls_bp.route('/<int:poll_id>/vote', methods=['POST'])
@login_required
def vote(poll_id):
    try:
        data = VoteSchema().load(request.json)
        poll_service.vote(poll_id, data['option'])
        return make_response(message='Ваш голос учтен'), 200
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@polls_bp.route('/<int:poll_id>/results', methods=['GET'])
def get_results(poll_id):
    try:
        results = poll_service.get_results(poll_id)
        return make_response(results=results), 200
    except Exception as e:
        return make_response(message=str(e)), 500
