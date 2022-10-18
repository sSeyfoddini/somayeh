import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.course_level_service import CourseLevelService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

course_level_ns = Namespace(
    "course_level",
    description="CourseLevel related operations",
    decorators=[cors.crossdomain(origin="*")],
)

course_level_add = course_level_ns.model(
    "CourseLevelAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

course_level_edit = course_level_ns.model(
    "CourseLevelEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@course_level_ns.route("/<string:uuid>")
class CourseLevelRest(Resource):
    def options(self):
        pass

    @course_level_ns.doc("return a CourseLevel")
    def get(self, uuid):

        try:
            course_level = CourseLevelService.get(uuid)
            return course_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @course_level_ns.expect(course_level_edit)
    @course_level_ns.doc("Update a CourseLevel")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            course_level = CourseLevelService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return course_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @course_level_ns.doc("delete a CourseLevel")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            course_level = CourseLevelService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return course_level._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@course_level_ns.route("/")
class CourseLevelListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            course_levels, total_records, page = CourseLevelService.get_all_by_filter(filter_dict)
            if course_levels:
                return (
                    {
                        "data": [course_level._to_dict() for course_level in course_levels],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(course_levels),
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

    @course_level_ns.expect(course_level_add)
    @course_level_ns.doc("Create a CourseLevel")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("course_level", args)
            course_level = CourseLevelService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return course_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
