import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.badge_object_service import BadgeObjectService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

badge_object_ns = Namespace(
    "badge_object",
    description="badge_object related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_object_add = badge_object_ns.model(
    "badge_objectAdd",
    {
        "badge_def_uuid": fields.String(required=True),
        "learner_uuid": fields.String(required=True),
        "status": fields.String(required=True),
    },
)

badge_object_edit = badge_object_ns.model(
    "badge_objectEdit",
    {
        "badge_def_uuid": fields.String(required=True),
        "learner_uuid": fields.String(required=True),
        "status": fields.String(required=True),
    },
)

badge_object_bulk_delete = badge_object_ns.model("CredentialDefinitionBulkDelete", {
    "uuid": fields.List(fields.String(required=True))})


@badge_object_ns.route("/<string:uuid>")
class BadgeObjectRest(Resource):
    def options(self):
        pass

    @badge_object_ns.doc("return a badge_object")
    def get(self, uuid):
        try:
            badge_object = BadgeObjectService.get(uuid)
            return badge_object._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_object_ns.expect(badge_object_edit)
    @badge_object_ns.doc("Update a badge_object")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            badge_object = BadgeObjectService.update(user_id=user_id, user_name=username, uuid=uuid,
                                                                       args=args)
            return badge_object._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @badge_object_ns.doc("delete a badge_object")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            badge_object = BadgeObjectService.delete_by_uuid(user_id=user_id, user_name=username,
                                                                               uuid=uuid)
            return badge_object._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_object_ns.route("/")
class BadgeObjectListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            badge_objects, total_records, page = BadgeObjectService.get_all_by_filter(filter_dict)
            if badge_objects:
                return (
                    {
                        "data": [badge_object._to_dict() for badge_object in badge_objects],
                        "page": {"page_number": page, "records_of_page": len(badge_objects),
                                 "total_records": total_records},
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

    @badge_object_ns.expect(badge_object_add)
    @badge_object_ns.doc("Create a badge_object")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("badge_object",args)
            badge_object = BadgeObjectService.add(
                user_id=user_id,
                user_name=username,
                args=args
            )

            return badge_object._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            BadgeObjectService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@badge_object_ns.route("/bulk_delete")
class BadgeObjectBulkDeleteRest(Resource):
    def options(self):
        pass

    @badge_object_ns.expect(badge_object_bulk_delete)
    @badge_object_ns.doc("Delete a list of badge_object")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                BadgeObjectService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
