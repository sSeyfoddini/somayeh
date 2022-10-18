import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import AcademicInfoService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
academic_info_ns = Namespace(
    "academic_info",
    description="academic_info related operations",
    decorators=[cors.crossdomain(origin="*")],
)

academic_info_model = academic_info_ns.model("academic_info", {"term_code": fields.String(required=True)})


@academic_info_ns.route("/academic_info")
class AcademicInfo(Resource):
    def options(self):
        pass

    @academic_info_ns.expect(academic_info_model)
    @academic_info_ns.doc("fetch academic_info data")
    def get(self):
        args = request.get_json()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            academic_data = AcademicInfoService.get(args, page, limit)
            if academic_data:
                return academic_data, 200, {"content-type": "application/json"}

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}


        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
