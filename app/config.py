"""Flask configuration variables."""
import logging
import os
import logging
from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    DATA_BROKER_URL = environ.get("DATA_BROKER_URL")
    DATA_BROKER_TOKEN = environ.get("DATA_BROKER_TOKEN")
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    IMAGE_SIZE = environ.get("IMAGE_SIZE")
    IMAGE_HIGHT = environ.get("IMAGE_HIGHT")
    IMAGE_WIDTH = environ.get("IMAGE_WIDTH")
    IMAGES_S3_BUCKET = environ.get("IMAGES_S3_BUCKET")
    REGION = environ.get("REGION")
    SENDER = environ.get("SENDER")
    BADGER_USERNAME = environ.get("BADGER_USERNAME")
    BADGER_PASSWORD = environ.get("BADGER_PASSWORD")
    EMSI_CLIENT_ID = environ.get("EMSI_CLIENT_ID")
    EMSI_CLIENT_SECRET = environ.get("EMSI_CLIENT_SECRET")
    EMSI_SCOPE = environ.get("EMSI_SCOPE")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    logging.basicConfig(
        filename=environ.get("LOG_FILE"),
        level=logging._nameToLevel.get(environ.get("LOG_LEVEL")),
    )
    pocket_core_api_message = os.getenv("POCKET_CORE_BASE_URL") + "/messaging/send"
    pocket_core_api_credential = os.getenv("POCKET_CORE_BASE_URL") + "/credential/jsonld/real/issue"
    pocket_core_api_set_external_id = os.getenv("POCKET_CORE_BASE_URL") + "/connection/set_external_id"
    hash_list = ["first_name", "last_name", "address1", "city"]
