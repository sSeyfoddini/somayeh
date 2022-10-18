import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.term_service import TermService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

ns_term_ns = Namespace(
    "term",
    description="Term related operations",
    decorators=[cors.crossdomain(origin="*")],
)

term_add = ns_term_ns.model(
    "TermAdd",
    {
        "name": fields.String(required=True),
        "start_date": fields.Date(required=True),
        "end_date": fields.Date(required=True),
        "session_id": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
    },
)

term_edit = ns_term_ns.model(
    "TermEdit",
    {
        "name": fields.String(required=True),
        "start_date": fields.Date(required=True),
        "end_date": fields.Date(required=True),
        "session_id": fields.String(required=False),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "credential_type_id": fields.Integer(required=False),
        "parent_organization": fields.String(required=False),
    },
)

term_bulk_delete = ns_term_ns.model("TermBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@ns_term_ns.route("/<string:uuid>")
class TermRest(Resource):
    def options(self):
        pass

    @ns_term_ns.doc("return a Term")
    def get(self, uuid):
        try:
            term = TermService.get(uuid)
            return term._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @ns_term_ns.expect(term_edit)
    @ns_term_ns.doc("Update a Term")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            term = TermService.update(user_id=user_id, user_name=username, uuid=uuid, args=args)
            return term._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @ns_term_ns.doc("delete a Term")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            term = TermService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return term._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@ns_term_ns.route("/")
class TermListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            terms, total_records, page = TermService.get_all_by_filter(filter_dict)
            if terms:
                return (
                    {
                        "data": [term._to_dict() for term in terms],
                        "page": {"page_number": page, "records_of_page": len(terms), "total_records": total_records},
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

    @ns_term_ns.expect(term_add)
    @ns_term_ns.doc("Create a Term")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("term", args)
            term = TermService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                start_date=args.get("start_date"),
                end_date=args.get("end_date"),
                session_id=args.get("session_id"),
                type=args.get("type"),
                external_id=args.get("external_id"),
                credential_type_id=args.get("credential_type_id"),
                parent_organization=args.get("parent_organization")
            )

            return term._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            TermService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@ns_term_ns.route("/bulk_delete")
class TermBulkDeleteRest(Resource):
    def options(self):
        pass

    @ns_term_ns.expect(term_bulk_delete)
    @ns_term_ns.doc("Delete a list of Department")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                TermService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
