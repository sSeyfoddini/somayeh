import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import ProgramsService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
programs_ns = Namespace(
    "programs",
    description="programs related operations",
    decorators=[cors.crossdomain(origin="*")],
)

programs_model = programs_ns.model("programs", {"term_code": fields.String(required=True)})


@programs_ns.route("/programs")
class Programs(Resource):
    def options(self):
        pass

    @programs_ns.expect(programs_model)
    @programs_ns.doc("fetch programs data")
    def get(self):
        args = request.get_json()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            programs_data = ProgramsService.get(args, page, limit)
            if programs_data:
                return programs_data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}


        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
