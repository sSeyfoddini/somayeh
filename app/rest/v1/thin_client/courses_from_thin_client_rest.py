import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import CourseService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
courses_classes_levels_ns = Namespace(
    "course",
    description="courses related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@courses_classes_levels_ns.route("/course")
class CourseGet(Resource):
    def options(self):
        pass

    @courses_classes_levels_ns.doc("get all course data")
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            data = CourseService.get(page, limit)
            if data:
                return data, 200, {"content-type": "application/json"}

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
