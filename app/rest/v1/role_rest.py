import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.role_service import RoleService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

role_ns = Namespace(
    "role",
    description="Role related operations",
    decorators=[cors.crossdomain(origin="*")],
)

role_add = role_ns.model(
    "RoleAdd",
    {
        "name": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "credential_type_id": fields.String(required=False),
        "parent_organization": fields.String(required=False),
    },
)

role_edit = role_ns.model(
    "RoleEdit",
    {
        "name": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "credential_type_id": fields.String(required=False),
        "parent_organization": fields.String(required=False),
    },
)

role_bulk_delete = role_ns.model("RoleBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@role_ns.route("/<string:uuid>")
class RoleRest(Resource):
    def options(self):
        pass

    @role_ns.doc("return a Role")
    def get(self, uuid):
        try:
            role = RoleService.get(uuid)
            return role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @role_ns.expect(role_edit)
    @role_ns.doc("Update a Role")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            role = RoleService.update(user_id=user_id, user_name=username, uuid=uuid, args=args)
            return role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__) 
            raise e

    @role_ns.doc("delete a Role")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            role = RoleService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return role._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@role_ns.route("/")
class RoleListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            roles, total_records, page = RoleService.get_all_by_filter(filter_dict)
            if roles:
                return (
                    {
                        "data": [role._to_dict() for role in roles],
                        "page": {"page_number": page, "records_of_page": len(roles), "total_records": total_records},
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

    @role_ns.expect(role_add)
    @role_ns.doc("Create a Role")
    def post(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("role", args)

            role = RoleService.add(
                user_id=user_id,
                user_name=username,
                args=args
            )

            return role._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            RoleService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@role_ns.route("/bulk_delete")
class RoleBulkDeleteRest(Resource):
    def options(self):
        pass

    @role_ns.expect(role_bulk_delete)
    @role_ns.doc("Delete a list of Role")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                RoleService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
