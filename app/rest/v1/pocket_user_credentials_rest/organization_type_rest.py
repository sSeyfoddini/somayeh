import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.organization_type_services import OrganizationTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

organization_type_ns = Namespace(
    "organization_type",
    description="OrganizationType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

organization_type_add = organization_type_ns.model(
    "OrganizationTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "subtype_id": fields.Integer(required=True),
    },
)

organization_type_edit = organization_type_ns.model(
    "OrganizationTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "subtype_id": fields.Integer(required=True),
    },
)

organization_type_bulk_delete = organization_type_ns.model(
    "OrganizationTypeBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@organization_type_ns.route("/<string:uuid>")
class OrganizationTypeRest(Resource):
    def options(self):
        pass

    @organization_type_ns.doc("return a OrganizationType")
    def get(self, uuid):
        try:
            organization_type = OrganizationTypeService.get(uuid)
            return (
                organization_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_type_ns.expect(organization_type_edit)
    @organization_type_ns.doc("Update a OrganizationType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            organization_type = OrganizationTypeService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                organization_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_type_ns.doc("delete a OrganizationType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            organization_type = OrganizationTypeService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return (
                organization_type._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_type_ns.route("/")
class OrganizationTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            organization_types, total_records, page = OrganizationTypeService.get_all_by_filter(filter_dict)
            if organization_types:
                return (
                    {
                        "data": [organization_type._to_dict() for organization_type in organization_types],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(organization_types),
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

    @organization_type_ns.expect(organization_type_add)
    @organization_type_ns.doc("Create a OrganizationType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("organization_type", args)
            organization_type = OrganizationTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                subtype_id=args.get("subtype_id"),
            )

            return (
                organization_type._to_dict(),
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
            OrganizationTypeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_type_ns.route("/bulk_delete")
class OrganizationTypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @organization_type_ns.expect(organization_type_bulk_delete)
    @organization_type_ns.doc("Delete a list of organization type")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                OrganizationTypeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
