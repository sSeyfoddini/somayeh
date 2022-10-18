import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.persistence import get_models
from app.services.relations_service.credit_recognition_service import CreditRecognitionService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

relation_credit_recognition_ns = Namespace(
    "relation_credit_recognition",
    description="Relation credit_recognition related operations",
    decorators=[cors.crossdomain(origin="*")],
)

credit_recognition_add = relation_credit_recognition_ns.model(
    "credit_recognitionAdd",
    {
        "credit_recognition_type_id": fields.Integer(required=True),
        "credit_recognition_name": fields.String(required=True),
        "credit_recognition_category_id": fields.Integer(required=True),
        "credit_recognition_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)

credit_recognition_edit = relation_credit_recognition_ns.model(
    "credit_recognitionEdit",
    {
        "credit_recognition_type_id": fields.Integer(required=True),
        "credit_recognition_name": fields.String(required=True),
        "credit_recognition_category_id": fields.Integer(required=True),
        "credit_recognition_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)


@relation_credit_recognition_ns.route("/<int:id>")
class credit_recognitionRest(Resource):
    def options(self):
        pass

    @relation_credit_recognition_ns.doc("return a credit_recognition")
    def get(self, id):
        get_models()
        try:
            credit_recognition = CreditRecognitionService.get(id)
            return credit_recognition._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


    @relation_credit_recognition_ns.expect(credit_recognition_edit)
    @relation_credit_recognition_ns.doc("Update a credit_recognition")
    def put(self, id):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"


        try:
            # todo should check the permission here
            credit_recognition = CreditRecognitionService.update(
                user_id=user_id,
                user_name=username,
                id=id,
                args=args
            )
            return credit_recognition._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @relation_credit_recognition_ns.doc("delete a credit_recognition")
    def delete(self, id):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"


        try:
            credit_recognition = CreditRecognitionService.delete_by_id(user_id=user_id, user_name=username, id=id)
            return credit_recognition._to_dict(), 201, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@relation_credit_recognition_ns.route("/")
class credit_recognitionListRest(Resource):
    def options(self):
        pass

    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            credit_recognition = CreditRecognitionService.get_all(page, limit)
            if credit_recognition:
               return (
                    [credit_recognition._to_dict() for credit_recognition in credit_recognition],
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


    @relation_credit_recognition_ns.expect(credit_recognition_add)
    @relation_credit_recognition_ns.doc("Create a credit_recognition")
    def post(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            credit_recognition = CreditRecognitionService.add(
                user_id=user_id,
                user_name=username,
                credit_recognition_type_id=args.get("credit_recognition_type_id"),
                credit_recognition_name=args.get("credit_recognition_name"),
                credit_recognition_category_id=args.get("credit_recognition_category_id"),
                credit_recognition_keywords=args.get("credit_recognition_keywords"),
                conferring_credential=args.get("conferring_credential"),
                conferring_identifier=args.get("conferring_identifier"),
                supporting_credential=args.get("supporting_credential"),
            )

            return credit_recognition._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e