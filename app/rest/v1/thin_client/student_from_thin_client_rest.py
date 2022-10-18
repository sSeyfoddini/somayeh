import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import StudentService
from app.util.error_handlers import InternalServerError
from app.util.message import get_message
from app.util.param_util import get_param

_log = logging.getLogger(__name__)
students_ns = Namespace(
    "students",
    description="Students fetch related operations",
    decorators=[cors.crossdomain(origin="*")],
)

students_model = students_ns.model("StudentsFetch", {"email": fields.String(required=False)})


@students_ns.route("/students")
class Students(Resource):
    def options(self):
        pass

    @students_ns.expect(students_model)
    @students_ns.doc("fetch students data")
    def post(self):
        lang = request.cookies.get("lang")
        if lang is None:
            lang = get_param("lang")
        args = request.get_json()
        try:
            org_data = StudentService.get(args["email"])

            return org_data, 200, {"content-type": "application/json"}


        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
