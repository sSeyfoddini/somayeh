import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import EmployeeTitlesService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
ps_employee_ns = Namespace(
    "ps_employee_titles",
    description="employee titles related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@ps_employee_ns.route("/ps_employee_titles")
class EmployeeGet(Resource):
    def options(self):
        pass

    @ps_employee_ns.doc("get all employee titles data")
    def get(self):

        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            data = EmployeeTitlesService.get(page, limit)
            if data:
                return data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
