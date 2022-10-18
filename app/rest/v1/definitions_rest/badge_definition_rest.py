import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.definitions_service.badge_definition_service import BadgeDefinitionService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

badge_definition_ns = Namespace(
    "badge_definition",
    description="BadgeDefinition related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_definition_add = badge_definition_ns.model(
    "BadgeDefinitionAdd",
    {
        "badge_id": fields.Integer(required=True),
        "badge_name": fields.String(required=True),
    },
)

badge_definition_edit = badge_definition_ns.model(
    "BadgeDefinitionEdit",
    {
        "badge_id": fields.Integer(required=True),
        "badge_name": fields.String(required=True),
    },
)


@badge_definition_ns.route("/<string:uuid>")
class BadgeDefinitionRest(Resource):
    def options(self):
        pass

    @badge_definition_ns.doc("return a BadgeDefinition")
    def get(self, uuid):


        try:
            badge_definition = BadgeDefinitionService.get(uuid)
            return (
                badge_definition._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_definition_ns.expect(badge_definition_edit)
    @badge_definition_ns.doc("Update a BadgeDefinition")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"


        try:
            # todo should check the permission here
            badge_definition = BadgeDefinitionService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                badge_definition._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_definition_ns.doc("delete a badgeDefinition")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"


        try:
            badge_definition = BadgeDefinitionService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return (
                badge_definition._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_definition_ns.route("/")
class BadgeDefinitionListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            badge_definitions, total_records, page = BadgeDefinitionService.get_all_by_filter(filter_dict)
            if badge_definitions:
                return (
                   {
                    "data": [badge_definition._to_dict() for badge_definition in badge_definitions],
                    "page": {
                        "page_number": page,
                        "records_of_page": len(badge_definitions),
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

    @badge_definition_ns.expect(badge_definition_add)
    @badge_definition_ns.doc("Create a BadgeDefinition")
    def post(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("badge_definition", args)
            badge_definition = BadgeDefinitionService.add(
                user_id=user_id, user_name=username, badge_id=args.get("badge_id"), badge_name=args.get("badge_name"),
            )

            return (
                badge_definition._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


