import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.class_service import ClassService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

class_ns = Namespace(
    "class",
    description="class related operations",
    decorators=[cors.crossdomain(origin="*")],
)

class_add = class_ns.model(
    "ClassAdd",
    {
        "external_class_id": fields.String(required=True),
        "course_id": fields.Integer(required=True),
        "external_course_id": fields.String(required=False),
        "instructor_id": fields.Integer(required=True),
        "session_id": fields.Integer(required=True),
        "term_id": fields.Integer(required=True),
        "topic": fields.String(required=False),
        "reference_uri": fields.String(required=False),
        "delivery_id": fields.Integer(required=False),
        "location_id": fields.Integer(required=False)

    },
)

class_edit = class_ns.model(
    "CredentialTypeEdit",
    {
        "external_class_id": fields.String(required=True),
        "course_id": fields.Integer(required=True),
        "external_course_id": fields.String(required=False),
        "instructor_id": fields.Integer(required=True),
        "session_id": fields.Integer(required=True),
        "term_id": fields.Integer(required=True),
        "topic": fields.String(required=False),
        "reference_uri": fields.String(required=False),
        "delivery_id": fields.Integer(required=False),
        "location_id": fields.Integer(required=False)
    },
)

class_bulk_delete = class_ns.model("ClassBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@class_ns.route("/<string:uuid>")
class ClassRest(Resource):
    def options(self):
        pass

    @class_ns.doc("return a Class")
    def get(self, uuid):

        try:
            _class = ClassService.get(uuid)
            return _class._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @class_ns.expect(class_edit)
    @class_ns.doc("Update a Class")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            _class = ClassService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return _class._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @class_ns.doc("delete a Class")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            _class = ClassService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return _class._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@class_ns.route("/")
class ClassListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            classs, total_records, page = ClassService.get_all_by_filter(filter_dict)
            if classs:
                return (
                    {
                        "data": [_class._to_dict() for _class in classs],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(classs),
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

    @class_ns.expect(class_add)
    @class_ns.doc("Create a Class")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"

        try:
            CheckField.check_missing_field_and_field_type("class", args)
            _class = ClassService.add(
                user_id=user_id,
                user_name=username,
                external_class_id=args.get("external_class_id"),
                course_id=args.get("course_id"),
                external_course_id=args.get("external_course_id"),
                instructor_id=args.get("instructor_id"),
                session_id=args.get("session_id"),
                term_id=args.get("term_id"),
                topic=args.get("topic"),
                reference_uri=args.get("reference_uri"),
                delivery_id=args.get("delivery_id"),
                location_id=args.get("location_id")
            )

            return _class._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):

        try:
            ClassService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@class_ns.route("/bulk_delete")
class classBulkDeleteRest(Resource):
    def options(self):
        pass

    @class_ns.expect(class_bulk_delete)
    @class_ns.doc("Delete a list of Class")
    def delete(self):

        args = request.get_json()
        user_id= 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                ClassService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

