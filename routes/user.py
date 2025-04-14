from flask import Blueprint, jsonify
from core.services.platform_service import PlatformService
from core.utils.response import make_response

platform_bp = Blueprint('platform', __name__, url_prefix='/api/platform')
platform_service = PlatformService()

@platform_bp.route('/statistics', methods=['GET'])
def get_platform_statistics():
    try:
        statistics = platform_service.get_statistics()
        return make_response(statistics=statistics), 200
    except Exception as e:
        return make_response(message=str(e)), 500