import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.instructor_role_service import InstructorRoleService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

instructor_role_ns = Namespace(
    "instructor_role",
    description="InstructorRole related operations",
    decorators=[cors.crossdomain(origin="*")],
)

instructor_role_add = instructor_role_ns.model(
    "InstructorRoleAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

instructor_role_edit = instructor_role_ns.model(
    "InstructorRoleEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@instructor_role_ns.route("/<string:uuid>")
class InstructorRoleRest(Resource):
    def options(self):
        pass

    @instructor_role_ns.doc("return a InstructorRole")
    def get(self, uuid):
        try:
            instructor_role = InstructorRoleService.get(uuid)
            return instructor_role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @instructor_role_ns.expect(instructor_role_edit)
    @instructor_role_ns.doc("Update a InstructorRole")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            instructor_role = InstructorRoleService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args,
            )
            return instructor_role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @instructor_role_ns.doc("delete a InstructorRole")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            instructor_role = InstructorRoleService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return instructor_role._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@instructor_role_ns.route("/")
class InstructorRoleListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()

        try:
            instructor_roles, total_records, page = InstructorRoleService.get_all_by_filter(filter_dict)
            if instructor_roles:
                return (
                    {
                        "data": [instructor_role._to_dict() for instructor_role in instructor_roles],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(instructor_roles),
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

    @instructor_role_ns.expect(instructor_role_add)
    @instructor_role_ns.doc("Create a InstructorRole")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("instructor_role", args)
            instructor_role = InstructorRoleService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return instructor_role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
