import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.general_education_fulfillment_service import (
    GeneralEducationFulfillmentService,
)
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

general_education_fulfillment_ns = Namespace(
    "general_education_fulfillment",
    description="GeneralEducationFulfillment related operations",
    decorators=[cors.crossdomain(origin="*")],
)

general_education_fulfillment_add = general_education_fulfillment_ns.model(
    "GeneralEducationFulfillmentAdd",
    {
        "credential_type_id": fields.Integer(required=True),
        "credential_type_label": fields.String(required=True),
        "recognition_date": fields.Date(required=True),
        "term_id": fields.Integer(required=True),
        "term_label": fields.String(required=True),
        "gen_ed_id": fields.Integer(required=True),
        "credential_label": fields.String(required=True),
        "gen_ed_name": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(requred=True),
    },
)

general_education_fulfillment_edit = general_education_fulfillment_ns.model(
    "GeneralEducationFulfillmentEdit",
    {
        "credential_type_id": fields.Integer(required=True),
        "credential_type_label": fields.String(required=True),
        "recognition_date": fields.Date(required=True),
        "term_id": fields.Integer(required=True),
        "term_label": fields.String(required=True),
        "gen_ed_id": fields.Integer(required=True),
        "credential_label": fields.String(required=True),
        "gen_ed_name": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@general_education_fulfillment_ns.route("/<string:uuid>")
class GeneralEducationFulfillmentRest(Resource):
    def options(self):
        pass

    @general_education_fulfillment_ns.doc("return a GeneralEducationFulfillment")
    def get(self, uuid):

        try:
            general_education_fulfillment = GeneralEducationFulfillmentService.get(uuid)
            return (
                general_education_fulfillment._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_fulfillment_ns.expect(general_education_fulfillment_edit)
    @general_education_fulfillment_ns.doc("Update a GeneralEducationFulfillment")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            general_education_fulfillment = GeneralEducationFulfillmentService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                general_education_fulfillment._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_fulfillment_ns.doc("delete a GeneralEducationFulfillment")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            general_education_fulfillment = GeneralEducationFulfillmentService.delete(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                general_education_fulfillment._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@general_education_fulfillment_ns.route("/")
class GeneralEducationFulfillmentListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            general_education_fulfillments, total_records, page = GeneralEducationFulfillmentService.get_all_by_filter(filter_dict)
            if general_education_fulfillments:
                return (
                    {
                        "data": [
                            general_education_fulfillment._to_dict()
                            for general_education_fulfillment in general_education_fulfillments
                        ],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(general_education_fulfillments),
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

    @general_education_fulfillment_ns.expect(general_education_fulfillment_add)
    @general_education_fulfillment_ns.doc("Create a GeneralEducationFulfillment")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("general_education_fulfillment", args)
            general_education_fulfillment = GeneralEducationFulfillmentService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                credential_type_label=args.get("credential_type_label"),
                recognition_date=args.get("recognition_date"),
                term_id=args.get("term_id"),
                term_label=args.get("term_label"),
                gen_ed_id=args.get("gen_ed_id"),
                credential_label=args.get("credential_label"),
                gen_ed_name=args.get("gen_ed_name"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return (
                general_education_fulfillment._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
