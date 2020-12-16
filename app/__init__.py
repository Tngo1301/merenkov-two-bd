from flask import Flask
from app.config import Config
from flask_admin import Admin
# база данных
from flask_sqlalchemy import SQLAlchemy
# миграции баз данных
from flask_migrate import Migrate
# вход пользователя в систему
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os,logging
from flask_bootstrap import Bootstrap
from flask_moment import Moment





app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
login = LoginManager(app)

login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#админка

from app import routes, models,errors

if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

def create_app(config_class=Config):
    # ...
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app
