import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.instructor_service import InstructorService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

instructor_ns = Namespace(
    "instructor",
    description="Instructor related operations",
    decorators=[cors.crossdomain(origin="*")],
)

instructor_add = instructor_ns.model(
    "InstructorAdd",
    {
        "name": fields.String(required=True),
        "school_id": fields.Integer(required=False),
        "college_id": fields.Integer(required=True),
        "instructor_role_id": fields.Integer(required=True),
        "did": fields.String(required=False),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

instructor_edit = instructor_ns.model(
    "InstructorEdit",
    {
        "name": fields.String(required=True),
        "school_id": fields.Integer(required=False),
        "college_id": fields.Integer(required=True),
        "instructor_role_id": fields.Integer(required=True),
        "did": fields.String(required=False),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@instructor_ns.route("/<string:uuid>")
class InstructorRest(Resource):
    def options(self):
        pass

    @instructor_ns.doc("return a Instructor")
    def get(self, uuid):
        try:
            instructor = InstructorService.get(uuid)
            return instructor._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @instructor_ns.expect(instructor_edit)
    @instructor_ns.doc("Update a Instructor")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            instructor = InstructorService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return instructor._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @instructor_ns.doc("delete a Instructor")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            instructor = InstructorService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return instructor._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@instructor_ns.route("/")
class InstructorListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            instructors, total_records, page = InstructorService.get_all_by_filter(filter_dict)
            if instructors:
                return (
                    {
                        "data": [instructor._to_dict() for instructor in instructors],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(instructors),
                            "total_records": total_records,
                        },
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

    @instructor_ns.expect(instructor_add)
    @instructor_ns.doc("Create a Instructor")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("instructor", args)
            instructor = InstructorService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                school_id=args.get("school_id"),
                college_id=args.get("college_id"),
                instructor_role_id=args.get("instructor_role_id"),
                did=args.get("did"),
                reference_uri=args.get("reference_uri"),
                type=args.get("type"),
                external_id=args.get("external_id")
            )

            return instructor._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
