import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.badge_partner_service import BadgePartnerService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

badge_partner_ns = Namespace(
    "badge_partner",
    description="badge_partner related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_partner_add = badge_partner_ns.model(
    "badge_partnerAdd",
    {
        "name": fields.String(required=False),
        "url": fields.String(required=False),
    },
)

badge_partner_edit = badge_partner_ns.model(
    "badge_partnerEdit",
    {
        "name": fields.String(required=False),
        "url": fields.String(required=False),
    },
)

badge_partner_bulk_delete = badge_partner_ns.model("BadgePartnerBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@badge_partner_ns.route("/<string:uuid>")
class BadgePartnerRest(Resource):
    def options(self):
        pass

    @badge_partner_ns.doc("return a badge partner")
    def get(self, uuid):
        try:
            badge_partner = BadgePartnerService.get(uuid)
            return badge_partner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_partner_ns.expect(badge_partner_edit)
    @badge_partner_ns.doc("Update a badge_partner")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            badge_partner = BadgePartnerService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return badge_partner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_partner_ns.doc("delete a badge partner")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            badge_partner = BadgePartnerService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return badge_partner._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_partner_ns.route("/")
class BadgePartnerListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            badge_partners, total_records, page = BadgePartnerService.get_all_by_filter(filter_dict)
            if badge_partners:
                return (
                    {
                        "data": [badge_partner._to_dict() for badge_partner in badge_partners],
                        "page": {"page_number": page, "records_of_page": len(badge_partners), "total_records": total_records},
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

    @badge_partner_ns.expect(badge_partner_add)
    @badge_partner_ns.doc("Create a badge_partner")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("badge_partner", args)
            badge_partner = BadgePartnerService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                url=args.get("url")
            )

            return badge_partner._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            BadgePartnerService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

@badge_partner_ns.route("/bulk_delete")
class BadgePartnerBulkDeleteRest(Resource):
    def options(self):
        pass

    @badge_partner_ns.expect(badge_partner_bulk_delete)
    @badge_partner_ns.doc("Delete a list of badge partner")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                BadgePartnerService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
