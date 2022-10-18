import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.general_education_group_asu_service import (
    GeneralEducationGroupASUService,
)
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

general_education_group_asu_ns = Namespace(
    "general_education_group_asu",
    description="GeneralEducationGroupASU related operations",
    decorators=[cors.crossdomain(origin="*")],
)

general_education_group_asu_add = general_education_group_asu_ns.model(
    "GeneralEducationGroupASUAdd",
    {
        "name": fields.String(required=False),
        "description": fields.String(required=False),
        "external_id": fields.String(required=True),
        "gen_id_list": fields.Integer(required=True),
        "gen_code_list": fields.String(required=True),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
    },
)

general_education_group_asu_edit = general_education_group_asu_ns.model(
    "GeneralEducationGroupASUEdit",
    {
        "name": fields.String(required=False),
        "description": fields.String(required=False),
        "external_id": fields.String(required=True),
        "gen_id_list": fields.Integer(required=True),
        "gen_code_list": fields.String(required=True),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
    },
)

general_bulk_delete = general_education_group_asu_ns.model(
    "GeneralEducationGroupAsuBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@general_education_group_asu_ns.route("/<string:uuid>")
class GeneralEducationGroupASURest(Resource):
    def options(self):
        pass

    @general_education_group_asu_ns.doc("return a GeneralEducationGroupASU")
    def get(self, uuid):

        try:
            general_education_group_asu = GeneralEducationGroupASUService.get(uuid)
            return (
                general_education_group_asu._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_group_asu_ns.expect(general_education_group_asu_edit)
    @general_education_group_asu_ns.doc("Update a GeneralEducationGroupASU")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            general_education_group_asu = GeneralEducationGroupASUService.update(
                user_id=user_id, user_name=username, uuid=uuid, args=args
            )
            return (
                general_education_group_asu._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @general_education_group_asu_ns.doc("delete a GeneralEducationGroupASU")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            general_education_group_asu = GeneralEducationGroupASUService.delete_by_uuid(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                general_education_group_asu._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@general_education_group_asu_ns.route("/")
class GeneralEducationGroupASUListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            general_education_group_asus, total_records, page = GeneralEducationGroupASUService.get_all_by_filter(filter_dict)
            if general_education_group_asus:
                return (
                    {
                        "data": [
                            general_education_group_asu._to_dict()
                            for general_education_group_asu in general_education_group_asus
                        ],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(general_education_group_asus),
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

    @general_education_group_asu_ns.expect(general_education_group_asu_add)
    @general_education_group_asu_ns.doc("Create a GeneralEducationGroupASU")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("general_education_group_asu", args)
            general_education_group_asu = GeneralEducationGroupASUService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                external_id=args.get("external_id"),
                gen_id_list=args.get("gen_id_list"),
                gen_code_list=args.get("gen_code_list"),
                credential_type_id=args.get("credential_type_id"),
                parent_organization=args.get("parent_organization")
            )

            return (
                general_education_group_asu._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            GeneralEducationGroupASUService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@general_education_group_asu_ns.route("/bulk_delete")
class GeneralBulkDeleteRest(Resource):
    def options(self):
        pass

    @general_education_group_asu_ns.expect(general_bulk_delete)
    @general_education_group_asu_ns.doc("Delete a list of General Education Group Asu")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"

        try:
            for uuid in args["uuid"]:
                GeneralEducationGroupASUService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
