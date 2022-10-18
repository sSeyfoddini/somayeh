import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.coursework_type_service import CourseworkTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

coursework_type_ns = Namespace(
    "coursework_type",
    description="CourseworkType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

coursework_type_add = coursework_type_ns.model(
    "CourseworkTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

coursework_type_edit = coursework_type_ns.model(
    "CourseworkTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@coursework_type_ns.route("/<string:uuid>")
class CourseworkTypeRest(Resource):
    def options(self):
        pass

    @coursework_type_ns.doc("return a CourseworkType")
    def get(self, uuid):

        try:
            coursework_type = CourseworkTypeService.get(uuid)
            return coursework_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @coursework_type_ns.expect(coursework_type_edit)
    @coursework_type_ns.doc("Update a CourseworkType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            coursework_type = CourseworkTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return coursework_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @coursework_type_ns.doc("delete a CourseworkType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            coursework_type = CourseworkTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return coursework_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@coursework_type_ns.route("/")
class CourseworkTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            coursework_types, total_records, page = CourseworkTypeService.get_all_by_filter(filter_dict)
            if coursework_types:
                return (
                    {
                        "data": [coursework_type._to_dict() for coursework_type in coursework_types],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(coursework_types),
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

    @coursework_type_ns.expect(coursework_type_add)
    @coursework_type_ns.doc("Create a CourseworkType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("coursework_type", args)
            coursework_type = CourseworkTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return coursework_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
