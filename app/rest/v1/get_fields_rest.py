import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.persistence import get_models
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

field_ns = Namespace("field", description="get fields details", decorators=[cors.crossdomain(origin="*")])


@field_ns.route("/<string:cmd>")
class FieldlRest(Resource):
    def options(self):
        pass

    @field_ns.doc("return a fields details")
    def get(self, cmd):
        try:
            classes, models, table_names = get_models()
            for model in classes:
                if cmd == model.__tablename__:
                    return (
                        model.__table__.columns.keys(),
                        200,
                        {"content-type": "application/json"},
                    )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
