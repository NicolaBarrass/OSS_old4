from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
#from flask_login import LoginManager


IMAGE_FOLDER = os.path.join('static', 'images')

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
#images = Images(app)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#login = LoginManager(app)

from app import routes, models


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