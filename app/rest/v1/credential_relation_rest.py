import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.relations_service.credential_relation_service import CredentialRelationService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

credential_relation_ns = Namespace(
    "credential_relation",
    description="credential_relation related operations",
    decorators=[cors.crossdomain(origin="*")],
)

credential_relation_add = credential_relation_ns.model(
    "credential_relationAdd",
    {
        "relation_type": fields.String(required=True),
        "target_cred_type_uuid": fields.String(required=True)
    },
)

credential_relation_edit = credential_relation_ns.model(
    "credential_relationEdit",
    {
        "relation_type": fields.String(required=True),
        "target_cred_type_uuid": fields.String(required=True)
    },
)

credential_relation_bulk_delete = credential_relation_ns.model("credential_relationBulkDelete", {
    "uuid": fields.List(fields.String(required=True))})


@credential_relation_ns.route("/<string:uuid>")
class CredentialRelationRest(Resource):
    def options(self):
        pass

    @credential_relation_ns.doc("return a credential_relation")
    def get(self, uuid):
        try:
            credential_relation = CredentialRelationService.get(uuid)
            return credential_relation._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_relation_ns.expect(credential_relation_edit)
    @credential_relation_ns.doc("Update a credential_relation")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            credential_relation = CredentialRelationService.update(user_id=user_id, user_name=username, uuid=uuid,
                                                                   args=args)
            return credential_relation._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @credential_relation_ns.doc("delete a credential_relation")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            CredentialRelationService.delete_by_uuid(user_id=user_id, user_name=username,
                                                                           uuid=uuid)
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_relation_ns.route("/")
class CredentialRelationListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            credential_relations, total_records, page = CredentialRelationService.get_all_by_filter(filter_dict)
            if credential_relations:
                return (
                    {
                        "data": [credential_relation._to_dict() for credential_relation in credential_relations],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(credential_relations),
                            "total_records": total_records
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

    @credential_relation_ns.expect(credential_relation_add)
    @credential_relation_ns.doc("Create a credential_relation")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("credential_relation", args)
            credential_relation = CredentialRelationService.add(
                user_id=user_id,
                user_name=username,
                args=args
            )

            return credential_relation._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            CredentialRelationService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@credential_relation_ns.route("/bulk_delete")
class CredentialRelationBulkDeleteRest(Resource):
    def options(self):
        pass

    @credential_relation_ns.expect(credential_relation_bulk_delete)
    @credential_relation_ns.doc("Delete a list of credential_relation")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                CredentialRelationService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
