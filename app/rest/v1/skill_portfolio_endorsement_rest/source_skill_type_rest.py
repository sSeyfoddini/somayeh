import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.source_skill_type_service import SourceSkillTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

source_skill_type_ns = Namespace(
    "source_skill_type",
    description="SourceSkillType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

source_skill_type_add = source_skill_type_ns.model(
    "SourceSkillTypeAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "source_skill_library_id": fields.String(required=True),
        "external_id": fields.String(required=True),
        "reference_uri": fields.String(required=True),
        "category": fields.String(required=False),
        "occupations": fields.String(required=False),
        "employer": fields.String(required=False),
        "certifications": fields.String(requied=False),
        "keywords": fields.String(required=False),
        "type": fields.String(required=False),
    },
)

source_skill_type_edit = source_skill_type_ns.model(
    "SourceSkillTypeEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "source_skill_library_id": fields.String(required=True),
        "external_id": fields.String(required=True),
        "reference_uri": fields.String(required=True),
        "category": fields.String(required=False),
        "occupations": fields.String(required=False),
        "employer": fields.String(required=False),
        "certifications": fields.String(requied=False),
        "keywords": fields.String(required=False),
        "type": fields.String(required=False),
    },
)


@source_skill_type_ns.route("/<string:uuid>")
class SourceSkillTypeRest(Resource):
    def options(self):
        pass

    @source_skill_type_ns.doc("return a SourceSkillType")
    def get(self, uuid):
        try:
            source_skill_type = SourceSkillTypeService.get(uuid)
            return (
                source_skill_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @source_skill_type_ns.expect(source_skill_type_edit)
    @source_skill_type_ns.doc("Update a SourceSkillType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            source_skill_type = SourceSkillTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                source_skill_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e

    @source_skill_type_ns.doc("delete a SourceSkillType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            source_skill_type = SourceSkillTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                source_skill_type._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e


@source_skill_type_ns.route("/")
class SourceSkillTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            source_skill_types, total_records, page = SourceSkillTypeService.get_all_by_filter(filter_dict)
            if source_skill_types:
                return (
                    {
                        "data": [source_skill_type._to_dict() for source_skill_type in source_skill_types],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(source_skill_types),
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

    @source_skill_type_ns.expect(source_skill_type_add)
    @source_skill_type_ns.doc("Create a SourceSkillType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("source_skill_type", args)
            source_skill_type = SourceSkillTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                source_skill_library_id=args.get("source_skill_library_id"),
                external_id=args.get("external_id"),
                reference_uri=args.get("reference_uri"),
                category=args.get("category"),
                occupations=args.get("occupations"),
                employer=args.get("employer"),
                certifications=args.get("certifications"),
                keywords=args.get("keywords"),
                type=args.get("type")
            )

            return (
                source_skill_type._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
