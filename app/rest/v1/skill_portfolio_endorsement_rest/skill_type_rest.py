import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.skill_type_service import SkillTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

skill_type_ns = Namespace(
    "skill_type",
    description="SkillType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

skill_type_add = skill_type_ns.model(
    "SkillTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "category_id": fields.List(fields.String(), required=False),
        "category_name": fields.List(fields.String(), required=False),
        "Updates_for_POCKMMVP_1030": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "source_skill_type_id": fields.String(required=False),
        "occupation_ids": fields.String(required=False),
        "employer_ids": fields.String(required=False),
        "keywords": fields.List(fields.String(), required=False),
        "rsd": fields.String(required=False),
        "rsd_uri": fields.String(required=False),
    },
)

skill_type_edit = skill_type_ns.model(
    "SkillTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "category_id": fields.List(fields.String(), required=False),
        "category_name": fields.List(fields.String(), required=False),
        "Updates_for_POCKMMVP_1030": fields.String(required=False),
        "reference_url": fields.String(required=False),
        "source_skill_type_id": fields.String(required=False),
        "occupation_ids": fields.String(required=False),
        "employer_ids": fields.String(required=False),
        "keywords": fields.List(fields.String(), required=False),
        "rsd": fields.String(required=False),
        "rsd_uri": fields.String(required=False),
    },
)

skill_type_bulk_delete = skill_type_ns.model("SkillTypeBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@skill_type_ns.route("/<string:uuid>")
class SkillTypeRest(Resource):
    def options(self):
        pass

    @skill_type_ns.doc("return a SkillType")
    def get(self, uuid):
        try:
            skill_type = SkillTypeService.get(uuid)
            return skill_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_type_ns.expect(skill_type_edit)
    @skill_type_ns.doc("Update a SkillType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            skill_type = SkillTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return skill_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @skill_type_ns.doc("delete a SkillType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            skill_type = SkillTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return skill_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@skill_type_ns.route("/")
class SkillTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            skill_types, total_records, page = SkillTypeService.get_all_by_filter(filter_dict)
            if skill_types:
                return (
                    {
                        "data": [skill_type._to_dict() for skill_type in skill_types],
                        "page": {"page_number": page, "records_of_page": len(skill_types), "total_records": total_records},
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

    @skill_type_ns.expect(skill_type_add)
    @skill_type_ns.doc("Create a SkillType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("skill_type", args)
            skill_type = SkillTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                category_id=args.get("category_id"),
                category_name=args.get("category_name"),
                Updates_for_POCKMMVP_1030=args.get("Updates_for_POCKMMVP_1030"),
                reference_url=args.get("reference_url"),
                source_skill_type_id=args.get("source_skill_type_id"),
                occupation_ids=args.get("occupation_ids"),
                employer_ids=args.get("employer_ids"),
                keywords=args.get("keywords"),
                rsd=args.get("rsd"),
                rsd_uri=args.get("rsd_uri"),
            )

            return skill_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            SkillTypeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@skill_type_ns.route("/bulk_delete")
class SkillTypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @skill_type_ns.expect(skill_type_bulk_delete)
    @skill_type_ns.doc("Delete a list of Skill Type")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                SkillTypeService.delete(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
