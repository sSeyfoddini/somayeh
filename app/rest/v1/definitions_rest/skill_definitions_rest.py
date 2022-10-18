import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.definitions_service.skill_definitions_service import SkillDefinitionsService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

skill_definitions_ns = Namespace(
    "skill_definitions",
    description="SkillDefinitions related operations",
    decorators=[cors.crossdomain(origin="*")],
)

skill_definitions_add = skill_definitions_ns.model(
    "SkillDefinitionsAdd",
    {
        "external_id": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "category": fields.String(required=True),
        "reference_url": fields.String(required=False),
        "keywords": fields.String(required=False),
        "course_code": fields.String(required=False),
        "occupation_ids": fields.String(required=False),
        "employer_ids": fields.String(requied=True),
    },
)

skill_definitions_edit = skill_definitions_ns.model(
    "SkillDefinitionsEdit",
    {
        "external_id": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "category": fields.String(required=True),
        "reference_url": fields.String(required=False),
        "keywords": fields.String(required=False),
        "course_code": fields.String(required=False),
        "occupation_ids": fields.String(required=False),
        "employer_ids": fields.String(requied=True),
    },
)


@skill_definitions_ns.route("/<int:uuid>")
class SkillDefinitionsRest(Resource):
    @skill_definitions_ns.doc("return a SkillDefinitions")
    def get(self, uuid):

        try:
            skill_definitions = SkillDefinitionsService.get(uuid)
            return (
                skill_definitions._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_definitions_ns.expect(skill_definitions_edit)
    @skill_definitions_ns.doc("Update a SkillDefinitions")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            skill_definitions = SkillDefinitionsService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                skill_definitions._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_definitions_ns.doc("delete a SkillDefinitions")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            skill_definitions = SkillDefinitionsService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                skill_definitions._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@skill_definitions_ns.route("/")
class SkillDefinitionsListRest(Resource):
    def get(self):
        filter_dict = request.args.to_dict()
        try:
            skill_definitionss, total_records, page = SkillDefinitionsService.get_all_by_filter(filter_dict)
            if skill_definitionss:
               return (
                   {
                      "data": [skill_definitions._to_dict() for skill_definitions in skill_definitionss],
                      "page": {"page_number": page,
                               "records_of_page": len(skill_definitionss),
                               "total_records": total_records},
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

    @skill_definitions_ns.expect(skill_definitions_add)
    @skill_definitions_ns.doc("Create a SkillDefinitions")
    def post(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("skill_definitions", args)
            skill_definitions = SkillDefinitionsService.add(
                user_id=user_id,
                user_name=username,
                external_id=args.get("external_id"),
                name=args.get("name"),
                description=args.get("description"),
                category=args.get("category"),
                reference_url=args.get("reference_url"),
                keywords=args.get("keywords"),
                course_code=args.get("course_code"),
                occupation_ids=args.get("occupation_ids"),
                employer_ids=args.get("employer_ids"),
            )

            return (
                skill_definitions._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e