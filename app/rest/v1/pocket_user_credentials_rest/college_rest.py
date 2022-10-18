import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.college_services import CollegeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

college_ns = Namespace(
    "college",
    description="College related operations",
    decorators=[cors.crossdomain(origin="*")],
)

college_add = college_ns.model(
    "CollegeAdd",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for college"),
        "college_id": fields.Integer(required=True, description="id of the college or school"),
        "college_label": fields.String(required=True, description="name of college"),
        "date": fields.Date(required=True, description="date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False)
    },
)

college_edit = college_ns.model(
    "CollegeEdit",
    {
        "credential_type_id": fields.Integer(required=True, description="type of credential, always id for college"),
        "college_id": fields.Integer(required=True, description="id of the college or school"),
        "college_label": fields.String(required=True, description="name of college"),
        "date": fields.Date(required=True, description="date credential was issued"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
        "parent_organization": fields.String(required=False),
    },
)

college_bulk_delete = college_ns.model("CollegeBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@college_ns.route("/<string:uuid>")
class CollegeRest(Resource):
    def options(self):
        pass

    @college_ns.doc("return a College")
    def get(self, uuid):
        try:
            college = CollegeService.get(uuid)
            return college._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @college_ns.expect(college_edit)
    @college_ns.doc("Update a College")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            college = CollegeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return college._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @college_ns.doc("delete a College")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            college = CollegeService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return college._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@college_ns.route("/")
class CollegeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            colleges, total_records, page = CollegeService.get_all_by_filter(filter_dict)
            if colleges:
                return (
                    {
                        "data": [college._to_dict() for college in colleges],
                        "page": {"page_number": page, "records_of_page": len(colleges), "total_records": total_records},
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

    @college_ns.expect(college_add)
    @college_ns.doc("Create a College")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("college", args)
            college = CollegeService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                college_id=args.get("college_id"),
                college_label=args.get("college_label"),
                date=args.get("date"),
                type=args.get("type"),
                external_id=args.get("external_id"),
                parent_organization=args.get("parent_organization")
            )

            return college._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            CollegeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@college_ns.route("/bulk_delete")
class CollegeBulkDeleteRest(Resource):
    def options(self):
        pass

    @college_ns.expect(college_bulk_delete)
    @college_ns.doc("Delete a list of college")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                CollegeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
