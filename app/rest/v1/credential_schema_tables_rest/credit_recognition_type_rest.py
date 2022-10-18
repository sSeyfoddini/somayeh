import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.credit_recognition_type_service import CreditRecognitionTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

credit_recognition_type_ns = Namespace(
    "credit_recognition_type",
    description="CreditRecognitionType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

credit_recognition_type_add = credit_recognition_type_ns.model(
    "CreditRecognitionTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

credit_recognition_type_edit = credit_recognition_type_ns.model(
    "CreditRecognitionTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@credit_recognition_type_ns.route("/<string:uuid>")
class CreditRecognitionTypeRest(Resource):
    def options(self):
        pass

    @credit_recognition_type_ns.doc("return a CreditRecognitionType")
    def get(self, uuid):

        try:
            credit_recognition_type = CreditRecognitionTypeService.get(uuid)
            return (
                credit_recognition_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credit_recognition_type_ns.expect(credit_recognition_type_edit)
    @credit_recognition_type_ns.doc("Update a CreditRecognitionType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            credit_recognition_type = CreditRecognitionTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                credit_recognition_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credit_recognition_type_ns.doc("delete a CreditRecognitionType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            credit_recognition_type = CreditRecognitionTypeService.delete(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                credit_recognition_type._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credit_recognition_type_ns.route("/")
class CreditRecognitionTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            credit_recognition_types, total_records, page = CreditRecognitionTypeService.get_all_by_filter(filter_dict)
            if credit_recognition_types:
                return (
                    {
                        "data": [
                            credit_recognition_type._to_dict() for credit_recognition_type in credit_recognition_types
                        ],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(credit_recognition_type_edit),
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

    @credit_recognition_type_ns.expect(credit_recognition_type_add)
    @credit_recognition_type_ns.doc("Create a CreditRecognitionType")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("credit_recognition_type", args)
            credit_recognition_type = CreditRecognitionTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return (
                credit_recognition_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
