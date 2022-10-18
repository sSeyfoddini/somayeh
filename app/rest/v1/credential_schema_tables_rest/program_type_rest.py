import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.program_type_service import ProgramTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

program_type_ns = Namespace(
    "program_type",
    description="ProgramType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

program_type_add = program_type_ns.model(
    "ProgramTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

program_type_edit = program_type_ns.model(
    "ProgramTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@program_type_ns.route("/<string:uuid>")
class ProgramTypeRest(Resource):
    def options(self):
        pass

    @program_type_ns.doc("return a ProgramType")
    def get(self, uuid):
        try:
            program_type = ProgramTypeService.get(uuid)
            return program_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_type_ns.expect(program_type_edit)
    @program_type_ns.doc("Update a ProgramType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            program_type = ProgramTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return program_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @program_type_ns.doc("delete a ProgramType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            program_type = ProgramTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return program_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@program_type_ns.route("/")
class ProgramTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            program_types, total_records, page = ProgramTypeService.get_all_by_filter(filter_dict)
            if program_types:
                return (
                    {
                        "data": [program_type._to_dict() for program_type in program_types],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(program_types),
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

    @program_type_ns.expect(program_type_add)
    @program_type_ns.doc("Create a ProgramType")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("program_type", args)
            program_type = ProgramTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return program_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
