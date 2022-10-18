import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.general_education_service import GeneralEducationService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

general_education_ns = Namespace(
    "general_education",
    description="GeneralEducation related operations",
    decorators=[cors.crossdomain(origin="*")],
)

general_education_add = general_education_ns.model(
    "GeneralEducationAdd",
    {
        "name": fields.String(required=True),
        "abbreviation": fields.String(required=False),
        "description": fields.String(required=False),
        "label": fields.String(required=True),
        "college_id": fields.Integer(required=False),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

general_education_edit = general_education_ns.model(
    "GeneralEducationEdit",
    {
        "name": fields.String(required=True),
        "abbreviation": fields.String(required=False),
        "description": fields.String(required=False),
        "label": fields.String(required=True),
        "college_id": fields.Integer(required=False),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@general_education_ns.route("/<string:uuid>")
class GeneralEducationRest(Resource):
    def options(self):
        pass

    @general_education_ns.doc("return a GeneralEducation")
    def get(self, uuid):

        try:
            general_education = GeneralEducationService.get(uuid)
            return (
                general_education._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_ns.expect(general_education_edit)
    @general_education_ns.doc("Update a GeneralEducation")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            general_education = GeneralEducationService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                general_education._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_ns.doc("delete a GeneralEducation")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            general_education = GeneralEducationService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                general_education._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@general_education_ns.route("/")
class GeneralEducationListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            general_educations, total_records, page = GeneralEducationService.get_all_by_filter(filter_dict)
            if general_educations:
                return (
                    {
                        "data": [general_education._to_dict() for general_education in general_educations],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(general_educations),
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

    @general_education_ns.expect(general_education_add)
    @general_education_ns.doc("Create a GeneralEducation")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"

        try:
            CheckField.check_missing_field_and_field_type("general_education", args)
            general_education = GeneralEducationService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                abbreviation=args.get("abbreviation"),
                description=args.get("description"),
                label=args.get("label"),
                college_id=args.get("college_id"),
                reference_uri=args.get("reference_uri"),
                type=args.get("type"),
                external_id=args.get("external_id")
            )

            return (
                general_education._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
