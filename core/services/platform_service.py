from flask import request, jsonify
from core.blueprints.platform import platform_blueprint
from core.utils import get_current_timestamp
import datetime

class PlatformService:
    @platform_blueprint.route('/time', methods=['GET'])
    def get_server_time():
        current_time = get_current_timestamp()
        return jsonify({'serverTime': current_time}), 200

    @platform_blueprint.route('/version', methods=['GET'])
    def get_version():
        version = '1.0.0' #Замените на актуальную версию
        return jsonify({'version': version}), 200