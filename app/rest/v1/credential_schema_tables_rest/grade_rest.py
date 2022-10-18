import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.grade_service import GradeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

grade_ns = Namespace(
    "grade",
    description="Grade related operations",
    decorators=[cors.crossdomain(origin="*")],
)

grade_add = grade_ns.model(
    "GradeAdd",
    {
        "letter": fields.String(required=True),
        "value": fields.Float(required=True),
        "description": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

grade_edit = grade_ns.model(
    "GradeEdit",
    {
        "letter": fields.String(required=True),
        "value": fields.Float(required=True),
        "description": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@grade_ns.route("/<string:uuid>")
class GradeRest(Resource):
    def options(self):
        pass

    @grade_ns.doc("return a Grade")
    def get(self, uuid):
        try:
            grade = GradeService.get(uuid)
            return grade._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @grade_ns.expect(grade_edit)
    @grade_ns.doc("Update a Grade")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            grade = GradeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return grade._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @grade_ns.doc("delete a Grade")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            grade = GradeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return grade._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@grade_ns.route("/")
class GradeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()

        try:
            grades, total_records, page = GradeService.get_all_by_filter(filter_dict)
            if grades:
                return (
                    {
                        "data": [grade._to_dict() for grade in grades],
                        "page": {"page_number": page, "records_of_page": len(grades), "total_records": total_records},
                    },
                    200,
                    {"content-type": "application/json"},
                )
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @grade_ns.expect(grade_add)
    @grade_ns.doc("Create a Grade")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("grade", args)
            grade = GradeService.add(
                user_id=user_id,
                user_name=username,
                letter=args.get("letter"),
                value=args.get("value"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return grade._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
