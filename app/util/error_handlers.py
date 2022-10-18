from enum import Enum
from flask import Blueprint

error_handler_bluprint = Blueprint('error_handlers', __name__)


class ErrorCodes(Enum):
    DB_ERROR = 3000
    INTERNAL_SERVER_ERROR = 3001
    RECORD_NOT_FOUND = 3002
    INVALID_IMAGE = 3003
    INVALID_FIELDS = 3004


class RecordNotFound(Exception):
    def __init__(self, message):
        self.status_code = ErrorCodes.RECORD_NOT_FOUND.value
        self.message = message


class DbConnectionError(Exception):
    def __init__(self, message):
        self.status_code = ErrorCodes.DB_ERROR.value
        self.message = message


class InternalServerError(Exception):
    def __init__(self, message):
        self.status_code = ErrorCodes.INTERNAL_SERVER_ERROR.value
        self.message = message


class InvalidImage(Exception):
    def __init__(self, message):
        self.status_code = ErrorCodes.INVALID_IMAGE.value
        self.message = message


class InvalidField(Exception):
    def __init__(self, message):
        self.status_code = ErrorCodes.INVALID_FIELDS.value
        self.message = message


@error_handler_bluprint.app_errorhandler(RecordNotFound)
def handle_record_not_found(error):
    payload = RecordNotFound(error.message)
    return payload.__dict__, 404, {"content-type": "application/json"}


@error_handler_bluprint.app_errorhandler(DbConnectionError)
def handle_db_connection_error(error):
    payload = DbConnectionError(error.message)
    return payload.__dict__, 503, {"content-type": "application/json"}


@error_handler_bluprint.app_errorhandler(InvalidField)
def handle_invalid_field(error):
    payload = InvalidField(error.message)
    return payload.__dict__, 400, {"content-type": "application/json"}


@error_handler_bluprint.app_errorhandler(InvalidImage)
def handle_invalid_image(error):
    payload = InvalidImage(error.message)
    return payload.__dict__, 500, {"content-type": "application/json"}


@error_handler_bluprint.app_errorhandler(InternalServerError)
def handle_exception(error):
    payload = InternalServerError(error.message)
    return payload.__dict__, 500, {"content-type": "application/json"}
