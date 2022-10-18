import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.program_services import ProgramService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

program_ns = Namespace(
    "program",
    description="Program related operations",
    decorators=[cors.crossdomain(origin="*")],
)

program_add = program_ns.model(
    "ProgramAdd",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for program"),
        "program_id": fields.Integer(required=True, description="id of the program"),
        "program_label": fields.String(required=True, description="Name of program"),
        "external_id": fields.String(required=True, description="Name of program"),
        "program_type_label": fields.String(required=True, description="Name of program"),
        "date": fields.Date(required=True, description="Date credential was issued"),
        "type": fields.String(required=False),
        "parent_organization": fields.String(required=False)
    },
)

program_edit = program_ns.model(
    "ProgramEdit",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for program"),
        "program_id": fields.Integer(required=True, description="id of the program"),
        "program_label": fields.String(required=True, description="Name of program"),
        "external_id": fields.String(required=True, description="Name of program"),
        "program_type_label": fields.String(required=True, description="Name of program"),
        "date": fields.Date(required=True, description="Date credential was issued"),
        "type": fields.String(required=False),
        "parent_organization": fields.String(required=False),
    },
)

program_bulk_delete = program_ns.model("ProgramBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@program_ns.route("/<string:uuid>")
class ProgramRest(Resource):
    def options(self):
        pass

    @program_ns.doc("return a Program")
    def get(self, uuid):
        try:
            program = ProgramService.get(uuid)
            return program._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_ns.expect(program_edit)
    @program_ns.doc("Update a Program")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            program = ProgramService.update(user_id=user_id, user_name=username, uuid=uuid, args=args)
            return program._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_ns.doc("delete a Program")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            program = ProgramService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return program._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@program_ns.route("/")
class ProgramListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            programs, total_records, page = ProgramService.get_all_by_filter(filter_dict)
            if programs:
                return (
                    {
                        "data": [program._to_dict() for program in programs],
                        "page": {"page_number": page, "records_of_page": len(programs), "total_records": total_records},
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

    @program_ns.expect(program_add)
    @program_ns.doc("Create a Program")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("program", args)
            program = ProgramService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                program_id=args.get("program_id"),
                program_label=args.get("program_label"),
                external_id=args.get("external_id"),
                program_type_label=args.get("program_type_label"),
                date=args.get("date"),
                type=args.get("type"),
                parent_organization=args.get("parent_organization"),
            )

            return program._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            ProgramService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@program_ns.route("/bulk_delete")
class ProgramBulkDeleteRest(Resource):
    def options(self):
        pass

    @program_ns.expect(program_bulk_delete)
    @program_ns.doc("Delete a list of Program")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                ProgramService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
