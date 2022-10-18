import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.course_service import CourseService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

course_ns = Namespace(
    "course",
    description="Course related operations",
    decorators=[cors.crossdomain(origin="*")],
)

course_add = course_ns.model(
    "CourseAdd",
    {
        "external_id": fields.String(required=True),
        "subject_code": fields.String(required=True),
        "catalog_code": fields.String(required=True),
        "reference_uri": fields.String(required=False),
        "college_id": fields.Integer(required=False),
        "school_id": fields.Integer(required=False),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "credit_hours": fields.Float(required=True),
        "course_level_id": fields.Integer(required=False),
        "general_ed_id_required": fields.Integer(required=False),
        "general_ed_id_credit": fields.Integer(required=False),
        "program_id_required": fields.String(required=False),
        "program_id_credit": fields.String(required=False),
        "type": fields.String(required=False),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
        "key": fields.String(required=True),
    },
)

course_edit = course_ns.model(
    "CourseEdit",
    {
        "external_id": fields.String(required=True),
        "subject_code": fields.String(required=True),
        "catalog_code": fields.String(required=True),
        "reference_uri": fields.String(required=False),
        "college_id": fields.Integer(required=False),
        "school_id": fields.Integer(required=False),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "credit_hours": fields.Float(required=True),
        "course_level_id": fields.Integer(required=False),
        "general_ed_id_required": fields.Integer(required=False),
        "general_ed_id_credit": fields.Integer(required=False),
        "program_id_required": fields.String(required=False),
        "program_id_credit": fields.String(required=False),
        "type": fields.String(required=False),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
        "key": fields.String(required=True),
    },
)

course_bulk_delete = course_ns.model("CourseBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@course_ns.route("/<string:uuid>")
class CourseRest(Resource):
    def options(self):
        pass

    @course_ns.doc("return a Course")
    def get(self, uuid):

        try:
            course = CourseService.get(uuid)
            return course._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @course_ns.expect(course_edit)
    @course_ns.doc("Update a Course")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            course = CourseService.update(user_id=user_id, user_name=username, uuid=uuid, args=args)
            return course._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @course_ns.doc("delete a Course")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            course = CourseService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return course._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@course_ns.route("/")
class CourseListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            courses, total_records, page = CourseService.get_all_by_filter(filter_dict)
            if courses:
                return (
                    {
                        "data": [course._to_dict() for course in courses],
                        "page": {"page_number": page, "records_of_page": len(courses), "total_records": total_records},
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

    @course_ns.expect(course_add)
    @course_ns.doc("Create a Course")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("course", args)
            course = CourseService.add(
                user_id=user_id,
                user_name=username,
                external_id=args.get("external_id"),
                subject_code=args.get("subject_code"),
                catalog_code=args.get("catalog_code"),
                reference_uri=args.get("reference_uri"),
                college_id=args.get("college_id"),
                school_id=args.get("school_id"),
                name=args.get("name"),
                description=args.get("description"),
                credit_hours=args.get("credit_hours"),
                course_level_id=args.get("course_level_id"),
                general_ed_id_required=args.get("general_ed_id_required"),
                general_ed_id_credit=args.get("general_ed_id_credit"),
                program_id_required=args.get("program_id_required"),
                program_id_credit=args.get("program_id_credit"),
                type=args.get("type"),
                credential_type_id=args.get("credential_type_id"),
                parent_organization=args.get("parent_organization"),
                key=args.get("key")
            )

            return course._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            CourseService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@course_ns.route("/bulk_delete")
class CourseBulkDeleteRest(Resource):
    def options(self):
        pass

    @course_ns.expect(course_bulk_delete)
    @course_ns.doc("Delete a list of Course")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                CourseService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
