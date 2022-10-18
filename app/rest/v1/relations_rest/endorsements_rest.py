import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.persistence import get_models
from app.services.relations_service.endorsements_service import EndorsementsService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

relation_endorsements_ns = Namespace(
    "relation_endorsements",
    description="Relation endorsements related operations",
    decorators=[cors.crossdomain(origin="*")],
)

endorsement_add = relation_endorsements_ns.model(
    "endorsementAdd",
    {
        "endorsement_type_id": fields.Integer(required=True),
        "endorsement_name": fields.String(required=True),
        "endorsement_category_id": fields.Integer(required=True),
        "endorsement_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)

endorsement_edit = relation_endorsements_ns.model(
    "endorsementEdit",
    {
        "endorsement_type_id": fields.Integer(required=True),
        "endorsement_name": fields.String(required=True),
        "endorsement_category_id": fields.Integer(required=True),
        "endorsement_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)


@relation_endorsements_ns.route("/<int:id>")
class endorsementRest(Resource):
    def options(self):
        pass

    @relation_endorsements_ns.doc("return a endorsement")
    def get(self, id):
        get_models()

        try:
            endorsement = EndorsementsService.get(id)
            return endorsement._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
    @relation_endorsements_ns.expect(endorsement_edit)
    @relation_endorsements_ns.doc("Update a endorsement")
    def put(self, id):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"


        try:
            # todo should check the permission here
            endorsement = EndorsementsService.update(
                user_id=user_id,
                user_name=username,
                id=id,
                args=args
            )
            return endorsement._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


    @relation_endorsements_ns.doc("delete a endorsement")
    def delete(self, id):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"


        try:
            endorsement = EndorsementsService.delete_by_id(user_id=user_id, user_name=username, id=id)
            return endorsement._to_dict(), 201, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e



@relation_endorsements_ns.route("/")
class endorsementListRest(Resource):
    def options(self):
        pass

    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:

            endorsements = EndorsementsService.get_all(page, limit)
            if endorsements:
                return (
                    [endorsement._to_dict() for endorsement in endorsements],
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



    @relation_endorsements_ns.expect(endorsement_add)
    @relation_endorsements_ns.doc("Create a endorsement")
    def post(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            endorsement = EndorsementsService.add(
                user_id=user_id,
                user_name=username,
                endorsement_type_id=args.get("endorsement_type_id"),
                endorsement_name=args.get("endorsement_name"),
                endorsement_category_id=args.get("endorsement_category_id"),
                endorsement_keywords=args.get("endorsement_keywords"),
                conferring_credential=args.get("conferring_credential"),
                conferring_identifier=args.get("conferring_identifier"),
                supporting_credential=args.get("supporting_credential"),
            )

            return endorsement._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

