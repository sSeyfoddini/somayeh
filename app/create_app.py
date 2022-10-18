"""Initialize Flask app."""
import logging

from flask import Flask

from app import db
from app.config import Config
from app.rest.api_v1 import api_v1
from app.util.error_handlers import error_handler_bluprint

_log = logging.getLogger(__name__)


def create_app():
    print("ali")
    """Construct the core application."""
    _log.info("start create the app.")

    app = Flask(__name__, instance_relative_config=False)
    # migrate = Migrate(app, db)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_v1)
    app.register_blueprint(error_handler_bluprint)

    return app
