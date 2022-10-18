import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.organization_subtype_services import OrganizationSubtypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

organization_subtype_ns = Namespace(
    "organization_subtype",
    description="OrganizationSubtype related operations",
    decorators=[cors.crossdomain(origin="*")],
)

organization_subtype_add = organization_subtype_ns.model(
    "OrganizationSubtypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "subtype_id": fields.Integer(required=True),
    },
)

organization_subtype_edit = organization_subtype_ns.model(
    "OrganizationSubtypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "subtype_id": fields.Integer(required=True),
    },
)

organization_subtype_bulk_delete = organization_subtype_ns.model(
    "OrganizationSubtypeBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@organization_subtype_ns.route("/<string:uuid>")
class OrganizationSubtypeRest(Resource):
    def options(self):
        pass

    @organization_subtype_ns.doc("return a OrganizationSubtype")
    def get(self, uuid):
        try:
            organization_subtype = OrganizationSubtypeService.get(uuid)
            return (
                organization_subtype._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_subtype_ns.expect(organization_subtype_edit)
    @organization_subtype_ns.doc("Update a OrganizationSubtype")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"
        try:
            # todo should check the permission here
            organization_subtype = OrganizationSubtypeService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                organization_subtype._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_subtype_ns.doc("delete a OrganizationSubtype")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            organization_subtype = OrganizationSubtypeService.delete_by_uuid(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                organization_subtype._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_subtype_ns.route("/")
class OrganizationSubtypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            organization_subtypes, total_records, page = OrganizationSubtypeService.get_all_by_filter(filter_dict)
            if organization_subtypes:
                return (
                    {
                        "data": [organization_subtype._to_dict() for organization_subtype in organization_subtypes],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(organization_subtypes),
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

    @organization_subtype_ns.expect(organization_subtype_add)
    @organization_subtype_ns.doc("Create a OrganizationSubtype")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("organization_subtype", args)
            organization_subtype = OrganizationSubtypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                subtype_id=args.get("subtype_id"),
            )

            return (
                organization_subtype._to_dict(),
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
            OrganizationSubtypeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_subtype_ns.route("/bulk_delete")
class OrganizationSubtypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @organization_subtype_ns.expect(organization_subtype_bulk_delete)
    @organization_subtype_ns.doc("Delete a list of organization subtype")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                OrganizationSubtypeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
