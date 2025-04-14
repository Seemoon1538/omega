import os
from app import create_app

config_name = os.getenv('FLASK_CONFIG') or 'default'  # получаем конфигурацию из переменной окружения
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)