import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.skill_category_service import SkillCategoryService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

skill_category_ns = Namespace(
    "skill_category",
    description="SkillCategory related operations",
    decorators=[cors.crossdomain(origin="*")],
)

skill_category_add = skill_category_ns.model(
    "SkillCategoryAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "reference_uri": fields.String(required=False),
    },
)

skill_category_edit = skill_category_ns.model(
    "SkillCategoryEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "reference_uri": fields.String(required=False),
    },
)


@skill_category_ns.route("/<string:uuid>")
class SkillCategoryRest(Resource):
    def options(self):
        pass

    @skill_category_ns.doc("return a SkillCategory")
    def get(self, uuid):

        try:
            skill_category = SkillCategoryService.get(uuid)
            return skill_category._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_category_ns.expect(skill_category_edit)
    @skill_category_ns.doc("Update a SkillCategory")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            skill_category = SkillCategoryService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return skill_category._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_category_ns.doc("delete a SkillCategory")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            skill_category = SkillCategoryService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return skill_category._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@skill_category_ns.route("/")
class SkillCategoryListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            skill_categorys, total_records, page = SkillCategoryService.get_all_by_filter(filter_dict)
            if skill_categorys:
                return (
                    {
                        "data": [skill_category._to_dict() for skill_category in skill_categorys],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(skill_categorys),
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

    @skill_category_ns.expect(skill_category_add)
    @skill_category_ns.doc("Create a SkillCategory")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("skill_category", args)
            skill_category = SkillCategoryService.add(
                user_name=username,
                user_id=user_id,
                name=args.get("name"),
                description=args.get("description"),
                reference_uri=args.get("reference_uri")
            )

            return skill_category._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
