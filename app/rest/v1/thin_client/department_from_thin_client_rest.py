import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import DepartmentService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
ps_department_ns = Namespace(
    "ps_department",
    description="department related operations",
    decorators=[cors.crossdomain(origin="*")],
)
department_model = ps_department_ns.model("ps_department", {"max_date": fields.Integer(required=True)})


@ps_department_ns.expect(department_model)
@ps_department_ns.route("/ps_department")
class ClassTableGet(Resource):
    def options(self):
        pass

    @ps_department_ns.doc("get all department data")
    def get(self):
        args = request.get_json()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            data = DepartmentService.get(args, page, limit)
            if data:
                return data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
