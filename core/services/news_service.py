from flask import request, jsonify
from flask_login import login_required
from core.security import auth_service
from core.database.repository import NewsRepository
from core.security.requires_role import requires_role
from core.blueprints.news import news_blueprint
from core.exceptions import AuthenticationError, AuthorizationError, ValidationError


news_repository = NewsRepository()


@news_blueprint.route('/', methods=['POST'])
@login_required
@requires_role('admin')
def create_news():
    data = request.get_json()
    title = data.get('title')
    text = data.get('text')

    if not title or not text:
        return jsonify({'error': 'Missing title or text'}), 400

    new_news = news_repository.create(title, text)
    if new_news is None:
        return jsonify({'error': 'Failed to create news'}), 500

    return jsonify({'message': 'News created successfully', 'news_id': new_news.id}), 201


@news_blueprint.route('/', methods=['GET'])
def get_news():
    news_items = news_repository.get_all()
    return jsonify([news.to_dict() for news in news_items]), 200


@news_blueprint.route('/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    news_item = news_repository.get_by_id(news_id)
    if news_item is None:
        return jsonify({'error': 'News not found'}), 404
    return jsonify(news_item.to_dict()), 200


@news_blueprint.route('/<int:news_id>', methods=['PUT'])
@login_required
@requires_role('admin')
def update_news(news_id):
    data = request.get_json()
    title = data.get('title')
    text = data.get('text')

    if not title or not text:
        return jsonify({'error': 'Missing title or text'}), 400

    news_item = news_repository.get_by_id(news_id)
    if news_item is None:
        return jsonify({'error': 'News not found'}), 404

    updated_news = news_repository.update(news_id, title, text)
    if updated_news is None:
        return jsonify({'error': 'Failed to update news'}), 500

    return jsonify({'message': 'News updated successfully'}), 200


@news_blueprint.route('/<int:news_id>', methods=['DELETE'])
@login_required
@requires_role('admin')
def delete_news(news_id):
    news_item = news_repository.get_by_id(news_id)
    if news_item is None:
        return jsonify({'error': 'News not found'}), 404
    news_repository.delete(news_id)
    return jsonify({'message': 'News deleted successfully'}), 200