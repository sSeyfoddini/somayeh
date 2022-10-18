import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.organization_identity_services import OrganizationIdentityService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

organization_identity_ns = Namespace(
    "organization_identity",
    description="OrganizationIdentity related operations",
    decorators=[cors.crossdomain(origin="*")],
)

organization_identity_add = organization_identity_ns.model(
    "OrganizationIdentityAdd",
    {
        "credential_type_id": fields.Integer(required=True),
        "organization_label": fields.String(required=True),
        "abbreviation": fields.String(required=True),
        "organization_type_id": fields.Integer(required=True),
        "organization_type_label": fields.String(required=True),
        "organization_subtype_id": fields.Integer(required=True),
        "organization_subtype_label": fields.String(required=True),
        "organization_parent_id": fields.Integer(required=True),
        "organization_parent_label": fields.String(required=True),
        "logo": fields.String(required=False),
        "background": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "street_1": fields.String(requied=True),
        "street_2": fields.String(requied=False),
        "country": fields.String(requied=True),
        "city": fields.String(required=True),
        "region": fields.String(required=True),
        "postal_code": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(requiredd=True),
        "parent_organization": fields.String(required=False)
    },
)

organization_identity_edit = organization_identity_ns.model(
    "OrganizationIdentityEdit",
    {
        "credential_type_id": fields.Integer(required=True),
        "organization_label": fields.String(required=True),
        "abbreviation": fields.String(required=True),
        "organization_type_id": fields.Integer(required=True),
        "organization_type_label": fields.String(required=True),
        "organization_subtype_id": fields.Integer(required=True),
        "organization_subtype_label": fields.String(required=True),
        "organization_parent_id": fields.Integer(required=True),
        "organization_parent_label": fields.String(required=True),
        "logo": fields.String(required=False),
        "background": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "street_1": fields.String(requied=True),
        "street_2": fields.String(requied=False),
        "country": fields.String(requied=True),
        "city": fields.String(required=True),
        "region": fields.String(required=True),
        "postal_code": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

organization_bulk_delete = organization_identity_ns.model(
    "OrganizationBulkDelete", {"uuid": fields.List(fields.String(), required=True)}
)


@organization_identity_ns.route("/<string:uuid>")
class OrganizationIdentityRest(Resource):
    def options(self):
        pass

    @organization_identity_ns.doc("return a OrganizationIdentity")
    def get(self, uuid):
        try:
            organization_identity = OrganizationIdentityService.get(uuid)
            return (
                organization_identity._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_identity_ns.expect(organization_identity_edit)
    @organization_identity_ns.doc("Update a OrganizationIdentity")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            organization_identity = OrganizationIdentityService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                organization_identity._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @organization_identity_ns.doc("delete a OrganizationIdentity")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            organization_identity = OrganizationIdentityService.delete_by_uuid(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                organization_identity._to_dict(),
                204,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_identity_ns.route("/")
class OrganizationIdentityListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            organization_identitys, total_records, page = OrganizationIdentityService.get_all_by_filter(filter_dict)
            if organization_identitys:
                return (
                    {
                        "data": [organization_identity._to_dict() for organization_identity in organization_identitys],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(organization_identitys),
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

    @organization_identity_ns.expect(organization_identity_add)
    @organization_identity_ns.doc("Create a OrganizationIdentity")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("organization_identity", args)
            organization_identity = OrganizationIdentityService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                organization_label=args.get("organization_label"),
                abbreviation=args.get("abbreviation"),
                organization_type_id=args.get("organization_type_id"),
                organization_type_label=args.get("organization_type_label"),
                organization_subtype_id=args.get("organization_subtype_id"),
                organization_subtype_label=args.get("organization_subtype_label"),
                organization_parent_id=args.get("organization_parent_id"),
                organization_parent_label=args.get("organization_parent_label"),
                logo=args.get("logo"),
                background=args.get("background"),
                reference_url=args.get("reference_url"),
                street_1=args.get("street_1"),
                street_2=args.get("street_2"),
                country=args.get("country"),
                city=args.get("city"),
                region=args.get("region"),
                postal_code=args.get("postal_code"),
                type=args.get("type"),
                external_id=args.get("external_id"),
                parent_organization=args.get("parent_organization")
            )

            return (
                organization_identity._to_dict(),
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
            OrganizationIdentityService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@organization_identity_ns.route("/bulk_delete")
class OrganizationBulkDeleteRest(Resource):
    def options(self):
        pass

    @organization_identity_ns.expect(organization_bulk_delete)
    @organization_identity_ns.doc("Delete a list of Organization Identity")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                OrganizationIdentityService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
