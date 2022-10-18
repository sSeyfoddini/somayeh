import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.credential_type_service import CredentialTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

credential_type_ns = Namespace(
    "credential_type",
    description="CredentialType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

credential_type_add = credential_type_ns.model(
    "CredentialTypeAdd",
    {
        "credential_definition_uuid": fields.String(required=False),
        "name": fields.String(required=True),
        "credential_type": fields.String(required=False),
        "schema_uri": fields.String(required=False),
    },
)

credential_type_edit = credential_type_ns.model(
    "CredentialTypeEdit",
    {
        "credential_definition_uuid": fields.String(required=False),
        "name": fields.String(required=True),
        "credential_type": fields.String(required=False),
        "schema_uri": fields.String(required=False),
    },
)

credential_type_bulk_delete = credential_type_ns.model(
    "CredentialTypeBulkDelete", {"uuid": fields.List(fields.String(), required=True)}
)


@credential_type_ns.route("/<string:uuid>")
class CredentialTypeRest(Resource):
    def options(self):
        pass

    @credential_type_ns.doc("return a CredentialType")
    def get(self, uuid):

        try:
            credential_type = CredentialTypeService.get(uuid)
            return credential_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_type_ns.expect(credential_type_edit)
    @credential_type_ns.doc("Update a CredentialType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            credential_type = CredentialTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return credential_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_type_ns.doc("delete a CredentialType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            credential_type = CredentialTypeService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return credential_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_type_ns.route("/")
class CredentialTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            credential_types, total_records, page = CredentialTypeService.get_all_by_filter(filter_dict)
            if credential_types:
                return (
                    {
                        "data": [credential_type._to_dict() for credential_type in credential_types],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(credential_types),
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

    @credential_type_ns.expect(credential_type_add)
    @credential_type_ns.doc("Create a CredentialType")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("credential_type", args)
            credential_type = CredentialTypeService.add(
                user_id=user_id,
                user_name=username,
                credential_definition_uuid=args.get("credential_definition_uuid"),
                name=args.get("name"),
                credential_type=args.get("credential_type"),
                schema_uri=args.get("schema_uri"),
            )

            return credential_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            CredentialTypeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_type_ns.route("/bulk_delete")
class CredentialTypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @credential_type_ns.expect(credential_type_bulk_delete)
    @credential_type_ns.doc("Delete a list of Credential Type")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                credential_type = CredentialTypeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
