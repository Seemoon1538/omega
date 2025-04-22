from flask import Flask, request
import logging, os
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from core.database import db, init_db
from core.utils import configure_logging
from core.security import auth_service
from core.security.authorization import bp
from core.blueprints.user import user_blueprint
from core.database.repository.user_repository import UserRepository
from flask_cors import CORS

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def create_app(config_name='development'):
    app = Flask('omega')
    logging.basicConfig(filename='C:\\app.log', level=logging.DEBUG)
    
    if config_name not in config:
        logging.error(f"Invalid config: {config_name}")
        raise ValueError(f"Invalid config: {config_name}")
    
    app.config.from_object(config[config_name])
    logging.info(f"Loaded config: {config_name}")
    
    try:
        db.init_app(app)
        auth_service.init_app(app)
        configure_logging(app)
        CORS(app)
        app.register_blueprint(bp)
        app.register_blueprint(user_blueprint)
        
        with app.app_context():
            user_repository = UserRepository(db)
            init_db(app, db)
    except Exception as e:
        logging.error(f"App creation error: {e}")
        raise
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            app.logger.debug('Received: %s', data)
            username = data.get('username')
            password = data.get('password')
            if username == 'test' and password == 'test':
                return {'status': 'success', 'message': 'Logged in'}, 200
            return {'status': 'error', 'message': 'Invalid credentials'}, 401
        except Exception as e:
            app.logger.error('Error: %s', str(e))
            return {'status': 'error', 'message': 'Server error'}, 500
    
    @app.route('/test')
    def test():
        return 'OK'
    
    return app

# Создание приложения
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False))
