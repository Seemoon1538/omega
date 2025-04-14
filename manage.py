import os
import sys
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from app import create_app, db

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    manager.run()