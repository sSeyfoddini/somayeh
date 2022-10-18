import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.organization_level_services import OrganizationLevelService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

organization_level_ns = Namespace(
    "organization_level",
    description="OrganizationLevel related operations",
    decorators=[cors.crossdomain(origin="*")],
)

organization_level_add = organization_level_ns.model(
    "OrganizationLevelAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
    },
)

organization_level_edit = organization_level_ns.model(
    "OrganizationLevelEdit",
    {
        "uuid": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
    },
)

organization_level_bulk_delete = organization_level_ns.model(
    "OrganizationLevelBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@organization_level_ns.route("/<string:uuid>")
class OrganizationLevelRest(Resource):
    def options(self):
        pass

    @organization_level_ns.doc("return a OrganizationLevel")
    def get(self, uuid):

        try:
            organization_level = OrganizationLevelService.get(uuid)
            return (
                organization_level._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_level_ns.expect(organization_level_edit)
    @organization_level_ns.doc("Update a OrganizationLevel")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            organization_level = OrganizationLevelService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                organization_level._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_level_ns.doc("delete a OrganizationLevel")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"
        try:
            organization_level = OrganizationLevelService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return (
                organization_level._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_level_ns.route("/")
class OrganizationLevelListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            organization_levels, total_records, page = OrganizationLevelService.get_all_by_filter(filter_dict)
            if organization_levels:
                return (
                    {
                        "data": [organization_level._to_dict() for organization_level in organization_levels],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(organization_levels),
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

    @organization_level_ns.expect(organization_level_add)
    @organization_level_ns.doc("Create a OrganizationLevel")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("organization_level", args)
            organization_level = OrganizationLevelService.add(
                user_id=user_id, user_name=username, name=args.get("name"), description=args.get("description")
            )

            return (
                organization_level._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            OrganizationLevelService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

@organization_level_ns.route("/bulk_delete")
class OrganizationLevelBulkDeleteRest(Resource):
    def options(self):
        pass

    @organization_level_ns.expect(organization_level_bulk_delete)
    @organization_level_ns.doc("Delete a list of organization level")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"

        try:
            for uuid in args["uuid"]:
                OrganizationLevelService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
