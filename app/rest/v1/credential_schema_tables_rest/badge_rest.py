import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.badge_service import BadgeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

badge_ns = Namespace(
    "badge",
    description="Badge related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_add = badge_ns.model(
    "BadgeAdd",
    {
        "credential_type_id": fields.String(required=True),
        "credential_type_label": fields.String(required=True),
        "class_id": fields.String(required=True),
        "external_user_id": fields.String(required=True),
        "badge_type_uuid": fields.String(required=True),
        "badge_name": fields.String(required=True),
        "badge_description": fields.String(required=True),
        "badge_org_id": fields.String(required=True),
        "badge_org_label": fields.String(required=True),
        "badge_org_logo": fields.String(required=True),
        "badge_date": fields.String(required=True),
        "badge_external_link": fields.String(required=True),
        "badge_image": fields.String(required=True),
        "badge_json": fields.String(required=False),
        "key": fields.String(required=True),
        "learner_uuid": fields.String(required=False)
    },
)

badge_edit = badge_ns.model(
    "BadgeEdit",
    {
        "credential_type_id": fields.String(required=True),
        "credential_type_label": fields.String(required=True),
        "class_id": fields.String(required=True),
        "external_user_id": fields.String(required=True),
        "badge_type_id": fields.String(required=True),
        "badge_name": fields.String(required=True),
        "badge_description": fields.String(required=True),
        "badge_org_id": fields.String(required=True),
        "badge_org_label": fields.String(required=True),
        "badge_org_logo": fields.String(required=True),
        "badge_date": fields.String(required=True),
        "badge_external_link": fields.String(required=True),
        "badge_image": fields.String(required=True),
        "badge_json": fields.String(required=False),
        "key": fields.String(required=True),
        "learner_uuid": fields.String(required=False)
    },
)

badge_bulk_delete = badge_ns.model("BadgeBulkDelete", {"uuid": fields.List(fields.String(), required=True)})


@badge_ns.route("/<string:uuid>")
class BadgeRest(Resource):
    def options(self):
        pass

    @badge_ns.doc("return a Badge")
    def get(self, uuid):
        try:
            badge = BadgeService.get(uuid)
            return badge._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_ns.expect(badge_edit)
    @badge_ns.doc("Update a Badge")
    def put(self, uuid):
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        args = request.get_json()
        try:
            # todo should check the permission here
            invalid_image, badge = BadgeService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            if invalid_image is None:
                return badge._to_dict(), 200, {"content-type": "application/json"}
            else:
                return ({"code": 500, "message": f"image {invalid_image} is not valid"}, 500,
                        {"content-type": "application/json"})

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_ns.doc("delete a Badge")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            BadgeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return {}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_ns.route("/")
class BadgeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        if "only_uuid" in request.args:
            only_uuid = bool(request.args["only_uuid"])
            filter_dict.pop("only_uuid")

        else:
            only_uuid = False
        try:
            badges, total_records, page = BadgeService.get_all_by_filter(filter_dict, only_uuid)
            if badges:
                if only_uuid:
                    return (
                        {
                            "data": badges,
                            "page": {"page_number": page, "records_of_page": len(badges), "total_records": total_records},
                        },
                        200,
                        {"content-type": "application/json"},
                    )
                return (
                    {
                        "data": [badge._to_dict() for badge in badges],
                        "page": {"page_number": page, "records_of_page": len(badges), "total_records": total_records},
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

    @badge_ns.expect(badge_add)
    @badge_ns.doc("Create a Badge")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"

        try:
            CheckField.check_missing_field_and_field_type("badge", args)
            badge = BadgeService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                credential_type_label=args.get("credential_type_label"),
                class_id=args.get("class_id"),
                external_user_id=args.get("external_user_id"),
                badge_type_uuid=args.get("badge_type_uuid"),
                badge_name=args.get("badge_name"),
                badge_description=args.get("badge_description"),
                badge_org_id=args.get("badge_org_id"),
                badge_org_label=args.get("badge_org_label"),
                badge_org_logo=args.get("badge_org_logo"),
                badge_date=args.get("badge_date"),
                badge_external_link=args.get("badge_external_link"),
                badge_json=args.get("badge_json"),
                key=args.get("key"),
                learner_uuid=args.get("learner_uuid")
            )
            if badge:
                return badge._to_dict(), 200, {"content-type": "application/json"}
            else:
                return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            BadgeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_ns.route("/bulk_delete")
class BadgeBulkDeleteRest(Resource):
    def options(self):
        pass

    @badge_ns.expect(badge_bulk_delete)
    @badge_ns.doc("Delete a list of badges")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                BadgeService.delete(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_ns.route("/get_auto_issue_badgs/<string:email>")
class BadgeAutoIssueRest(Resource):
    def options(self):
        pass

    def get(self, email):
        try:
            badges = BadgeService.get_true_auto_issue_badges(email)
            return [badge._to_dict() for badge in badges]

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e