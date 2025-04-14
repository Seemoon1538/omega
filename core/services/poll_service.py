from flask import request, jsonify
from flask_login import login_required
from core.security import auth_service
from core.database.repository import PollRepository, PollOptionRepository, VoteRepository
from core.security.requires_role import requires_role
from core.blueprints.poll import poll_blueprint
from core.exceptions import AuthenticationError, AuthorizationError, ValidationError
from core.utils import is_valid_amount
import random


poll_repository = PollRepository()
poll_option_repository = PollOptionRepository()
vote_repository = VoteRepository()


@poll_blueprint.route('/', methods=['POST'])
@login_required
@requires_role('admin')
def create_poll():
    data = request.get_json()
    question = data.get('question')
    options = data.get('options')

    if not question or not options:
        return jsonify({'error': 'Missing question or options'}), 400

    if len(options) < 2:
        return jsonify({'error': 'At least two options are required'}), 400

    new_poll = poll_repository.create(question)
    if new_poll is None:
        return jsonify({'error': 'Failed to create poll'}), 500

    for option_text in options:
        new_option = poll_option_repository.create(new_poll.id, option_text)
        if new_option is None:
            return jsonify({'error': 'Failed to create poll option'}), 500

    return jsonify({'message': 'Poll created successfully', 'poll_id': new_poll.id}), 201


@poll_blueprint.route('/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = poll_repository.get_by_id(poll_id)
    if poll is None:
        return jsonify({'error': 'Poll not found'}), 404
    options = poll_option_repository.get_all_by_poll_id(poll_id)
    return jsonify({'poll': poll.to_dict(), 'options': [option.to_dict() for option in options]}), 200


@poll_blueprint.route('/<int:poll_id>/vote', methods=['POST'])
@login_required
def vote(poll_id):
    data = request.get_json()
    option_id = data.get('option_id')

    if not option_id:
        return jsonify({'error': 'Missing option_id'}), 400

    poll = poll_repository.get_by_id(poll_id)
    if poll is None:
        return jsonify({'error': 'Poll not found'}), 404

    option = poll_option_repository.get_by_id(option_id)
    if option is None:
        return jsonify({'error': 'Option not found'}), 404

    user_id = auth_service.get_jwt_identity()
    if vote_repository.get_by_user_id_and_poll_id(user_id, poll_id):
        return jsonify({'error': 'You have already voted in this poll'}), 400

    new_vote = vote_repository.create(user_id, poll_id, option_id)
    if new_vote is None:
        return jsonify({'error': 'Failed to create vote'}), 500

    return jsonify({'message': 'Vote submitted successfully'}), 201


@poll_blueprint.route('/<int:poll_id>/results', methods=['GET'])
def get_results(poll_id):
    poll = poll_repository.get_by_id(poll_id)
    if poll is None:
        return jsonify({'error': 'Poll not found'}), 404
    options = poll_option_repository.get_all_by_poll_id(poll_id)
    results = []
    for option in options:
        votes = vote_repository.get_count_by_option_id(option.id)
        results.append({'option_id': option.id, 'option_text': option.text, 'votes': votes})

    return jsonify(results), 200