import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.class_level_services import ClassLevelService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

class_level_ns = Namespace(
    "class_level",
    description="ClassLevel related operations",
    decorators=[cors.crossdomain(origin="*")],
)

class_level_add = class_level_ns.model(
    "ClassLevelAdd",
    {
        "level": fields.String(required=True, description="type of credential, always id for class_level"),
        "description": fields.String(required=False, description='Always "class_level"'),
        "semester_order": fields.Integer(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

class_level_edit = class_level_ns.model(
    "ClassLevelEdit",
    {
        "level": fields.String(required=True, description="type of credential, always id for class_level"),
        "description": fields.String(required=False, description='Always "class_level"'),
        "semester_order": fields.Integer(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@class_level_ns.route("/<string:uuid>")
class ClassLevelRest(Resource):
    def options(self):
        pass

    @class_level_ns.doc("return a ClassLevel")
    def get(self, uuid):

        try:
            class_level = ClassLevelService.get(uuid)
            return class_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @class_level_ns.expect(class_level_edit)
    @class_level_ns.doc("Update a ClassLevel")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            class_level = ClassLevelService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return class_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @class_level_ns.doc("delete a ClassLevel")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            class_level = ClassLevelService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return class_level._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@class_level_ns.route("/")
class ClassLevelListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            class_levels, total_records, page = ClassLevelService.get_all_by_filter(filter_dict)
            if class_levels:
                return (
                    {
                        "data": [class_level._to_dict() for class_level in class_levels],
                        "page": {"page_number": page, "records_of_page": len(class_levels), "total_records": total_records},
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

    @class_level_ns.expect(class_level_add)
    @class_level_ns.doc("Create a ClassLevel")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("class_level", args)
            class_level = ClassLevelService.add(
                user_id=user_id,
                user_name=username,
                level=args.get("level"),
                description=args.get("description"),
                semester_order=args.get("semester_order"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return class_level._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
