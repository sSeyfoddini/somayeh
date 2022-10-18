import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.source_skill_library_service import SourceSkillLibraryService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

source_skill_library_ns = Namespace(
    "source_skill_library",
    description="SourceSkillLibrary related operations",
    decorators=[cors.crossdomain(origin="*")],
)

source_skill_library_add = source_skill_library_ns.model(
    "SourceSkillLibraryAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "external_id": fields.String(required=True),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
    },
)

source_skill_library_edit = source_skill_library_ns.model(
    "SourceSkillLibraryEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "external_id": fields.String(required=True),
        "reference_uri": fields.String(required=False),
        "type": fields.String(required=False),
    },
)


@source_skill_library_ns.route("/<string:uuid>")
class SourceSkillLibraryRest(Resource):
    def options(self):
        pass

    @source_skill_library_ns.doc("return a SourceSkillLibrary")
    def get(self, uuid):
        try:
            source_skill_library = SourceSkillLibraryService.get(uuid)
            return (
                source_skill_library._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @source_skill_library_ns.expect(source_skill_library_edit)
    @source_skill_library_ns.doc("Update a SourceSkillLibrary")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            source_skill_library = SourceSkillLibraryService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return (
                source_skill_library._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e

    @source_skill_library_ns.doc("delete a SourceSkillLibrary")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            source_skill_library = SourceSkillLibraryService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return (
                source_skill_library._to_dict(),
                204,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@source_skill_library_ns.route("/")
class SourceSkillLibraryListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            source_skill_librarys, total_records, page = SourceSkillLibraryService.get_all_by_filter(filter_dict)
            if source_skill_librarys:
                return (
                    {
                        "data": [source_skill_library._to_dict() for source_skill_library in source_skill_librarys],
                        "page": {
                            "page_number": page,
                            "records_of_page": len(source_skill_librarys),
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

    @source_skill_library_ns.expect(source_skill_library_add)
    @source_skill_library_ns.doc("Create a SourceSkillLibrary")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("source_skill_library", args)
            source_skill_library = SourceSkillLibraryService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                external_id=args.get("external_id"),
                reference_uri=args.get("reference_uri"),
                type=args.get("type")
            )

            return (
                source_skill_library._to_dict(),
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
