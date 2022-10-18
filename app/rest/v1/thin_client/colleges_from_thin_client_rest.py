import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import CollegesService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
colleges_ns = Namespace(
    "colleges",
    description="colleges related operations",
    decorators=[cors.crossdomain(origin="*")],
)

colleges_model = colleges_ns.model("colleges", {"term_code": fields.String(required=True)})


@colleges_ns.route("/colleges")
class Colleges(Resource):
    def options(self):
        pass

    @colleges_ns.expect(colleges_model)
    @colleges_ns.doc("fetch colleges data")
    def get(self):
        args = request.get_json()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            colleges_data = CollegesService.get(args, page, limit)
            if colleges_data:
                return colleges_data, 200, {"content-type": "application/json"}

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
