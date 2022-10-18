import logging

from flask_restx import Namespace, Resource, cors

from app.persistence import get_models
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

model_ns = Namespace("model", description="get model details", decorators=[cors.crossdomain(origin="*")])


@model_ns.route("/<string:cmd>")
class ModelRest(Resource):
    def options(self):
        pass

    @model_ns.doc("return a model details")
    def get(self, cmd):

        try:
            classes, models, table_names = get_models()
            if cmd == "model":
                return models, 200, {"content-type": "application/json"}
            elif cmd == "table":
                return table_names, 200, {"content-type": "application/json"}
            elif cmd == "all":
                return (
                    {"models": models, "tables": table_names},
                    200,
                    {"content-type": "application/json"},
                )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)

            raise e
