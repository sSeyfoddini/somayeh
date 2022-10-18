import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.persistence import get_models
from app.services.relations_service.coursework_service import CourseworkService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

relation_coursework_ns = Namespace(
    "relation_coursework",
    description="Relation coursework related operations",
    decorators=[cors.crossdomain(origin="*")],
)

coursework_add = relation_coursework_ns.model(
    "courseworkAdd",
    {
        "coursework_type_id": fields.Integer(required=True),
        "coursework_name": fields.String(required=True),
        "coursework_category_id": fields.Integer(required=True),
        "coursework_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)

coursework_edit = relation_coursework_ns.model(
    "courseworkEdit",
    {
        "coursework_type_id": fields.Integer(required=True),
        "coursework_name": fields.String(required=True),
        "coursework_category_id": fields.Integer(required=True),
        "coursework_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)


@relation_coursework_ns.route("/<int:id>")
class courseworkRest(Resource):
    def options(self):
        pass

    @relation_coursework_ns.doc("return a coursework")
    def get(self, id):
        get_models()
        try:
            coursework = CourseworkService.get(id)
            return coursework._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @relation_coursework_ns.expect(coursework_edit)
    @relation_coursework_ns.doc("Update a coursework")
    def put(self, id):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            coursework = CourseworkService.update(
                user_id=user_id,
                user_name=username,
                id=id,
                args=args
            )
            return coursework._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @relation_coursework_ns.doc("delete a coursework")
    def delete(self, id):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            coursework = CourseworkService.delete_by_id(user_id=user_id, user_name=username, id=id)
            return coursework._to_dict(), 201, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@relation_coursework_ns.route("/")
class courseworkListRest(Resource):
    def options(self):
        pass

    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            coursework = CourseworkService.get_all(page, limit)
            if coursework:
                return (
                    [coursework._to_dict() for coursework in coursework],
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




    @relation_coursework_ns.expect(coursework_add)
    @relation_coursework_ns.doc("Create a coursework")
    def post(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            coursework = CourseworkService.add(
                user_id=user_id,
                user_name=username,
                coursework_type_id=args.get("coursework_type_id"),
                coursework_name=args.get("coursework_name"),
                coursework_category_id=args.get("coursework_category_id"),
                coursework_keywords=args.get("coursework_keywords"),
                conferring_credential=args.get("conferring_credential"),
                conferring_identifier=args.get("conferring_identifier"),
                supporting_credential=args.get("supporting_credential"),
            )

            return coursework._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e