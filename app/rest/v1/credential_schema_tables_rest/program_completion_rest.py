import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.program_completion_service import ProgramCompletionService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

program_completion_ns = Namespace(
    "program_completion",
    description="ProgramCompletion related operations",
    decorators=[cors.crossdomain(origin="*")],
)

program_completion_add = program_completion_ns.model(
    "ProgramCompletionAdd",
    {
        "credential_type_id": fields.Integer(required=True),
        "credential_type_label": fields.String(required=True),
        "recognition_date": fields.Date(required=True),
        "term_id": fields.Integer(required=True),
        "term_label": fields.String(required=True),
        "program_id": fields.Integer(required=True),
        "program_label": fields.String(required=True),
        "credential_label": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

program_completion_edit = program_completion_ns.model(
    "ProgramCompletionEdit",
    {
        "credential_type_id": fields.Integer(required=True),
        "credential_type_label": fields.String(required=True),
        "recognition_date": fields.Date(required=True),
        "term_id": fields.Integer(required=True),
        "term_label": fields.String(required=True),
        "program_id": fields.Integer(required=True),
        "program_label": fields.String(required=True),
        "credential_label": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@program_completion_ns.route("/<string:uuid>")
class ProgramCompletionRest(Resource):
    def options(self):
        pass

    @program_completion_ns.doc("return a ProgramCompletion")
    def get(self, uuid):

        try:
            program_completion = ProgramCompletionService.get(uuid)
            return (
                program_completion._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_completion_ns.expect(program_completion_edit)
    @program_completion_ns.doc("Update a ProgramCompletion")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            program_completion = ProgramCompletionService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                program_completion._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_completion_ns.doc("delete a ProgramCompletion")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            program_completion = ProgramCompletionService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                program_completion._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@program_completion_ns.route("/")
class ProgramCompletionListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            program_completions, total_records, page = ProgramCompletionService.get_all_by_filter(filter_dict)
            if program_completions:
                return (
                    {
                        "data": [program_completion._to_dict() for program_completion in program_completions],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(program_completions),
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

    @program_completion_ns.expect(program_completion_add)
    @program_completion_ns.doc("Create a ProgramCompletion")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("program_completion", args)
            program_completion = ProgramCompletionService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                credential_type_label=args.get("credential_type_label"),
                recognition_date=args.get("recognition_date"),
                term_id=args.get("term_id"),
                term_label=args.get("term_label"),
                program_id=args.get("program_id"),
                program_label=args.get("program_label"),
                credential_label=args.get("credential_label"),
                type=args.get("type"),
                external_id=args.get("external_id")
            )

            return (
                program_completion._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
