import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.definitions_service.credential_definition_service import CredentialDefinitionService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

credential_definition_ns = Namespace(
    "credential_definition",
    description="credential_definition related operations",
    decorators=[cors.crossdomain(origin="*")],
)

credential_definition_add = credential_definition_ns.model(
    "credential_definitionAdd",
    {
        "cred_def_type": fields.String(required=True),
        "cred_def": fields.String(required=True),
        "schema": fields.String(required=False),
        "name": fields.String(required=False)
    },
)

credential_definition_edit = credential_definition_ns.model(
    "credential_definitionEdit",
    {
        "cred_def_type": fields.String(required=True),
        "cred_def": fields.String(required=True),
        "schema": fields.String(required=False),
        "name": fields.String(required=False)
    },
)

credential_definition_bulk_delete = credential_definition_ns.model("CredentialDefinitionBulkDelete", {
    "uuid": fields.List(fields.String(required=True))})


@credential_definition_ns.route("/<string:uuid>")
class CredentialDefinitionRest(Resource):
    def options(self):
        pass

    @credential_definition_ns.doc("return a credential_definition")
    def get(self, uuid):
        try:
            credential_definition = CredentialDefinitionService.get(uuid)
            return credential_definition._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_definition_ns.expect(credential_definition_edit)
    @credential_definition_ns.doc("Update a credential_definition")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            credential_definition = CredentialDefinitionService.update(user_id=user_id, user_name=username, uuid=uuid,
                                                                       args=args)
            return credential_definition._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_definition_ns.doc("delete a credential_definition")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            credential_definition = CredentialDefinitionService.delete_by_uuid(user_id=user_id, user_name=username,
                                                                               uuid=uuid)
            return credential_definition._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_definition_ns.route("/")
class CredentialDefinitionListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            credential_definitions, total_records, page = CredentialDefinitionService.get_all_by_filter(filter_dict)
            if credential_definitions:
                return (
                    {
                        "data": [credential_definition._to_dict() for credential_definition in credential_definitions],
                        "page": {"page_number": page, "records_of_page": len(credential_definitions),
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

    @credential_definition_ns.expect(credential_definition_add)
    @credential_definition_ns.doc("Create a credential_definition")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("credential_definition", args)
            credential_definition = CredentialDefinitionService.add(
                user_id=user_id,
                user_name=username,
                args=args
            )

            return credential_definition._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            CredentialDefinitionService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
              e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_definition_ns.route("/bulk_delete")
class CredentialDefinitionBulkDeleteRest(Resource):
    def options(self):
        pass

    @credential_definition_ns.expect(credential_definition_bulk_delete)
    @credential_definition_ns.doc("Delete a list of credential_definition")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                CredentialDefinitionService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
