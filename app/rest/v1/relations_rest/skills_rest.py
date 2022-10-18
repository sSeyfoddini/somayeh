import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.persistence import get_models
from app.services.relations_service.skills_service import SkillService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

relation_skills_ns = Namespace(
    "relation_skills",
    description="Relation Skills related operations",
    decorators=[cors.crossdomain(origin="*")],
)

skill_add = relation_skills_ns.model(
    "SkillAdd",
    {
        "skill_type_id": fields.Integer(required=True),
        "skill_name": fields.String(required=True),
        "skill_category_id": fields.Integer(required=True),
        "skill_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)

skill_edit = relation_skills_ns.model(
    "SkillEdit",
    {
        "skill_type_id": fields.Integer(required=True),
        "skill_name": fields.String(required=True),
        "skill_category_id": fields.Integer(required=True),
        "skill_keywords": fields.String(required=False),
        "conferring_credential": fields.Integer(requied=True),
        "conferring_identifier": fields.Integer(requied=True),
        "supporting_credential": fields.Integer(requied=False),
    },
)


@relation_skills_ns.route("/<int:id>")
class SkillRest(Resource):
    def options(self):
        pass

    @relation_skills_ns.doc("return a Skill")
    def get(self, id):
        get_models()

        try:
            skill = SkillService.get(id)
            return skill._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @relation_skills_ns.expect(skill_edit)
    @relation_skills_ns.doc("Update a Skill")
    def put(self, id):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"


        try:
            # todo should check the permission here
            skill = SkillService.update(
                user_id=user_id,
                user_name=username,
                id=id,
                args=args
            )
            return skill._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
    @relation_skills_ns.doc("delete a Skill")
    def delete(self, id):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"


        try:
            skill = SkillService.delete_by_id(user_id=user_id, user_name=username, id=id)
            return skill._to_dict(), 201, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

@relation_skills_ns.route("/")
class SkillListRest(Resource):
    def options(self):
        pass

    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            skills = SkillService.get_all(page, limit)
            if skills:
               return (
                    [skill._to_dict() for skill in skills],
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


    @relation_skills_ns.expect(skill_add)
    @relation_skills_ns.doc("Create a Skill")
    def post(self):
        lang = request.cookies.get("lang")
        if lang is None:
            lang = get_param("lang")

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            skill = SkillService.add(
                user_id=user_id,
                user_name=username,
                skill_type_id=args.get("skill_type_id"),
                skill_name=args.get("skill_name"),
                skill_category_id=args.get("skill_category_id"),
                skill_keywords=args.get("skill_keywords"),
                conferring_credential=args.get("conferring_credential"),
                conferring_identifier=args.get("conferring_identifier"),
                supporting_credential=args.get("supporting_credential"),
            )

            return skill._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e