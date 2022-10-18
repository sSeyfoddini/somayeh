import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.department_services import DepartmentService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

department_ns = Namespace(
    "department",
    description="Department related operations",
    decorators=[cors.crossdomain(origin="*")],
)

department_add = department_ns.model(
    "DepartmentAdd",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for department"),
        "department_id": fields.Integer(required=True, description="id of the department"),
        "department_label": fields.String(required=True, description="Name of department"),
        "date": fields.Date(required=True, description="Date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

department_edit = department_ns.model(
    "DepartmentEdit",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for department"),
        "department_id": fields.Integer(required=True, description="id of the department"),
        "department_label": fields.String(required=True, description="Name of department"),
        "date": fields.Date(required=True, description="Date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

department_bulk_delete = department_ns.model(
    "DepartmentBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@department_ns.route("/<string:uuid>")
class DepartmentRest(Resource):
    def options(self):
        pass

    @department_ns.doc("return a Department")
    def get(self, uuid):
        try:
            department = DepartmentService.get(uuid)
            return department._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @department_ns.expect(department_edit)
    @department_ns.doc("Update a Department")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            department = DepartmentService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return department._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @department_ns.doc("delete a Department")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            department = DepartmentService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return department._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@department_ns.route("/")
class DepartmentListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            departments, total_records, page = DepartmentService.get_all_by_filter(filter_dict)
            if departments:
                return (
                    {
                        "data": [department._to_dict() for department in departments],
                        "page": {"page_number": page, "records_of_page": len(departments), "total_records": total_records},
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

    @department_ns.expect(department_add)
    @department_ns.doc("Create a Department")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("department", args)
            department = DepartmentService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                department_id=args.get("department_id"),
                department_label=args.get("department_label"),
                date=args.get("date"),
                type=args.get("type"),
                external_id=args.get("external_id"),
                parent_organization=args.get("parent_organization")
            )

            return department._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            DepartmentService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@department_ns.route("/bulk_delete")
class DepartmentBulkDeleteRest(Resource):
    def options(self):
        pass

    @department_ns.expect(department_bulk_delete)
    @department_ns.doc("Delete a list of Department")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                DepartmentService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
