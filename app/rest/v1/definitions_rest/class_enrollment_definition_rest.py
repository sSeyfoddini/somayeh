import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.definitions_service.class_enrollment_definition_service import ClassEnrollmentDefinitionService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

class_enrollment_definition_ns = Namespace(
    "class_enrollment_definition",
    description="ClassEnrollmentDefinition related operations",
    decorators=[cors.crossdomain(origin="*")],
)

class_enrollment_definition_add = class_enrollment_definition_ns.model(
    "ClassEnrollmentDefinitionAdd",
    {
        "course_id": fields.Integer(required=True),
        "course_subject": fields.String(required=True),
        "course_number": fields.String(required=True),
        "course_name": fields.String(required=True),
    },
)

class_enrollment_definition_edit = class_enrollment_definition_ns.model(
    "ClassEnrollmentDefinitionEdit",
    {
        "course_id": fields.Integer(required=True),
        "course_subject": fields.String(required=True),
        "course_number": fields.String(required=True),
        "course_name": fields.String(required=True),
    },
)


@class_enrollment_definition_ns.route("/<string:uuid>")
class ClassEnrollmentDefinitionRest(Resource):
    def options(self):
        pass

    @class_enrollment_definition_ns.doc("return a ClassEnrollmentDefinition")
    def get(self, uuid):

        try:
            class_enrollment_definition = ClassEnrollmentDefinitionService.get(uuid)
            return (
                class_enrollment_definition._to_dict(),
                200,
                {"content-type": "application/json"},
             )
        except Exception as e:
              if "status_code" not in e.__dict__:
                 e = InternalServerError(str(e.args[0]))
              _log.error(e.__dict__)
              raise e

    @class_enrollment_definition_ns.expect(class_enrollment_definition_edit)
    @class_enrollment_definition_ns.doc("Update a ClassEnrollmentDefinition")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            class_enrollment_definition = ClassEnrollmentDefinitionService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                class_enrollment_definition._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @class_enrollment_definition_ns.doc("delete a class_enrollmentDefinition")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            class_enrollment_definition = ClassEnrollmentDefinitionService.delete_by_uuid(
                user_id=user_id, user_name=username, uuid=uuid
            )
            return (
                class_enrollment_definition._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@class_enrollment_definition_ns.route("/")
class ClassEnrollmentDefinitionListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            class_enrollment_definitions, total_records, page = ClassEnrollmentDefinitionService.get_all_by_filter(filter_dict)
            if class_enrollment_definitions:
                return (
                    {
                        "data": [
                            class_enrollment_definition._to_dict()
                            for class_enrollment_definition in class_enrollment_definitions
                        ],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(class_enrollment_definitions),
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
    @class_enrollment_definition_ns.expect(class_enrollment_definition_add)
    @class_enrollment_definition_ns.doc("Create a class_enrollmentDefinition")
    def post(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("class_enrollment_definition", args)
            class_enrollment_definition = ClassEnrollmentDefinitionService.add(
                user_id=user_id,
                user_name=username,
                course_id=args.get("course_id"),
                course_subject=args.get("course_subject"),
                course_number=args.get("course_number"),
                course_name=args.get("course_name"),
            )

            return (
                class_enrollment_definition._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e