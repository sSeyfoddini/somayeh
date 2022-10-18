import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.school_services import SchoolService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

school_ns = Namespace(
    "school",
    description="School related operations",
    decorators=[cors.crossdomain(origin="*")],
)

school_add = school_ns.model(
    "SchoolAdd",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for school"),
        "school_id": fields.Integer(required=True, description="id of the school or department"),
        "school_label": fields.String(required=True, description="name of school or department"),
        "date": fields.Date(required=True, description="date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

school_edit = school_ns.model(
    "SchoolEdit",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for school"),
        "school_id": fields.Integer(required=True, description="id of the school or department"),
        "school_label": fields.String(required=True, description="name of school or department"),
        "date": fields.Date(required=True, description="date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

school_bulk_delete = school_ns.model("SchoolBulkDelete", {"uuid": fields.List(fields.String(), required=True)})


@school_ns.route("/<string:uuid>")
class SchoolRest(Resource):
    def options(self):
        pass

    @school_ns.doc("return a School")
    def get(self, uuid):
        try:
            school = SchoolService.get(uuid)
            return school._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @school_ns.expect(school_edit)
    @school_ns.doc("Update a School")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            school = SchoolService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return school._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @school_ns.doc("delete a School")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            school = SchoolService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return school._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@school_ns.route("/")
class SchoolListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            schools, total_records, page = SchoolService.get_all_by_filter(filter_dict)
            if schools:
                return (
                    {
                        "data": [school._to_dict() for school in schools],
                        "page": {"page_number": page, "records_of_page": len(schools), "total_records": total_records},
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

    @school_ns.expect(school_add)
    @school_ns.doc("Create a School")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("school", args)
            school = SchoolService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                school_id=args.get("school_id"),
                school_label=args.get("school_label"),
                date=args.get("date"),
                type=args.get("type"),
                external_id=args.get("external_id"),
                parent_organization=args.get("parent_organization")
            )

            return school._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            SchoolService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@school_ns.route("/bulk_delete")
class SchoolBulkDeleteRest(Resource):
    def options(self):
        pass

    @school_ns.expect(school_bulk_delete)
    @school_ns.doc("Delete a list of School")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                school = SchoolService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
