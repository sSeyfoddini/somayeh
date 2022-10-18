import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.experience_category_service import ExperienceCategoryService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

experience_category_ns = Namespace(
    "experience_category",
    description="experience category related operations",
    decorators=[cors.crossdomain(origin="*")],
)

experience_category_add = experience_category_ns.model(
    "ExperienceCategoryAdd",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "parent_name": fields.String(required=False),
        "parent_id": fields.Integer(required=False),
    },
)

experience_category_edit = experience_category_ns.model(
    "ExperienceCategoryEdit",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "parent_name": fields.String(required=False),
        "parent_id": fields.Integer(required=False),
    },
)

experience_bulk_delete = experience_category_ns.model(
    "ExperienceBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@experience_category_ns.route("/<string:uuid>")
class ExperienceCategoryRest(Resource):
    def options(self):
        pass

    @experience_category_ns.doc("return a experience_category")
    def get(self, uuid):
        try:
            experience = ExperienceCategoryService.get(uuid)
            return experience._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @experience_category_ns.expect(experience_category_edit)
    @experience_category_ns.doc("Update a experience_category")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            experience = ExperienceCategoryService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return experience._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @experience_category_ns.doc("delete a experience_category")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            experience = ExperienceCategoryService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return experience._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@experience_category_ns.route("/")
class ExperienceCategoryListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            experiences, total_records, page = ExperienceCategoryService.get_all_by_filter(filter_dict)
            if experiences:
                return (
                    {
                        "data": [experience._to_dict() for experience in experiences],
                        "page": {"page_number": page, "records_of_page": len(experiences), "total_records": total_records},
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

    @experience_category_ns.expect(experience_category_add)
    @experience_category_ns.doc("Create a experience_category")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("experience_category", args)
            experience = ExperienceCategoryService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                parent_name=args.get("parent_name"),
                parent_id=args.get("parent_id")
            )

            return experience._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            ExperienceCategoryService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@experience_category_ns.route("/bulk_delete")
class ExperienceCategoryBulkDeleteRest(Resource):
    def options(self):
        pass

    @experience_category_ns.expect(experience_bulk_delete)
    @experience_category_ns.doc("Delete a list of experience_category")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                experience = ExperienceCategoryService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
