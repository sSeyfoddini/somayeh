import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import SaGradeService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
sa_grade_ns = Namespace(
    "sa_grade",
    description="sa_grade related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@sa_grade_ns.route("/sa_grade")
class SaGradeGet(Resource):
    def options(self):
        pass

    @sa_grade_ns.doc("get all sa_grade data")
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            sa_grade_data = SaGradeService.get(page, limit)
            if sa_grade_data:
                return sa_grade_data, 200, {"content-type": "application/json"}

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}


        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
