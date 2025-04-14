from flask import Blueprint, request, jsonify
from core.services.news_service import NewsService
from core.utils.auth_utils import login_required, admin_required
from core.utils.response import make_response
from marshmallow import Schema, fields, ValidationError

news_bp = Blueprint('news', __name__, url_prefix='/api/news')
news_service = NewsService()

class NewsSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)

@news_bp.route('/', methods=['GET'])
def get_news():
    try:
        news_items = news_service.get_news()
        return make_response(news=[n.to_dict() for n in news_items]), 200
    except Exception as e:
        return make_response(message=str(e)), 500

@news_bp.route('/', methods=['POST'])
@admin_required
def create_news():
    try:
        data = NewsSchema().load(request.json)
        news_item = news_service.create_news(data['title'], data['content'])
        return make_response(news=news_item.to_dict()), 201
    except ValidationError as e:
        return make_response(errors=e.messages), 400
    except Exception as e:
        return make_response(message=str(e)), 500

@news_bp.route('/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    try:
        news_item = news_service.get_news_by_id(news_id)
        if not news_item:
            return make_response(message='Новость не найдена'), 404
        return make_response(news=news_item.to_dict()), 200
    except Exception as e:
        return make_response(message=str(e)), 500
