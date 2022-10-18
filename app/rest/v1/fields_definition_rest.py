import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.fields_definition_service import FieldsDefinitionService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

fields_definition_ns = Namespace(
    "fields_definition",
    description="fields definition related operations",
    decorators=[cors.crossdomain(origin="*")],
)

fields_definition_model = fields_definition_ns.model(
    "FieldsDefinition",
    {"credential": fields.String(required=True)},
)


@fields_definition_ns.route("/")
class FieldsDefinitionRest(Resource):
    def options(self):
        pass

    def post(self):
        args = request.get_json()
        table_name = args.get("credential")
        try:
            datas = FieldsDefinitionService.get(table_name)

            return datas, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
