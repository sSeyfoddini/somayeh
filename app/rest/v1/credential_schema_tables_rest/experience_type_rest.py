import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.credential_schema_tables_services.experience_type_service import ExperienceTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

experience_type_ns = Namespace(
    "experience_type",
    description="experience category related operations",
    decorators=[cors.crossdomain(origin="*")],
)

experience_type_add = experience_type_ns.model(
    "ExperienceTypeAdd",
    {
        "experience_type_id": fields.Integer(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "org_id": fields.Integer(required=True),
        "org_name": fields.String(required=True),
        "org_logo": fields.String(required=False),
        "experience_category_id": fields.String(required=True),
        "experience_category": fields.String(required=True),
        "experience_subcategory_id": fields.String(required=False),
        "experience_subcategory": fields.String(required=False),
        "image": fields.String(required=True),
    },
)

experience_type_edit = experience_type_ns.model(
    "ExperienceTypeEdit",
    {
        "experience_type_id": fields.Integer(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "org_id": fields.Integer(required=True),
        "org_name": fields.String(required=True),
        "org_logo": fields.String(required=False),
        "experience_category_id": fields.String(required=True),
        "experience_category": fields.String(required=True),
        "experience_subcategory_id": fields.String(required=False),
        "experience_subcategory": fields.String(required=False),
        "image": fields.String(required=True),
    },
)

experience_bulk_delete = experience_type_ns.model(
    "ExperienceBulkDelete", {"uuid": fields.List(fields.String(required=True))}
)


@experience_type_ns.route("/<string:uuid>")
class ExperienceTypeRest(Resource):
    def options(self):
        pass

    @experience_type_ns.doc("return a experience_type")
    def get(self, uuid):

        try:
            experience = ExperienceTypeService.get(uuid)
            return experience._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @experience_type_ns.expect(experience_type_edit)
    @experience_type_ns.doc("Update a experience_type")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            experience = ExperienceTypeService.update(
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

    @experience_type_ns.doc("delete a experience_type")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            experience = ExperienceTypeService.delete_by_uuid(user_id=user_id, user_name=username, uuid=uuid)
            return experience._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@experience_type_ns.route("/")
class ExperienceTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            experiences, total_records, page = ExperienceTypeService.get_all_by_filter(filter_dict)
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

    @experience_type_ns.expect(experience_type_add)
    @experience_type_ns.doc("Create a experience_type")
    def post(self):

        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("experience_type", args)
            experience = ExperienceTypeService.add(
                user_id=user_id,
                user_name=username,
                experience_type_id=args.get("experience_type_id"),
                name=args.get("name"),
                description=args.get("description"),
                org_id=args.get("org_id"),
                org_name=args.get("org_name"),
                org_logo=args.get("org_logo"),
                experience_category_id=args.get("experience_category_id"),
                experience_category=args.get("experience_category"),
                experience_subcategory_id=args.get("experience_subcategory_id"),
                experience_subcategory=args.get("experience_subcategory"),
                image=args.get("image")
            )

            return experience._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            ExperienceTypeService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@experience_type_ns.route("/bulk_delete")
class ExperienceTypeBulkDeleteRest(Resource):
    def options(self):
        pass

    @experience_type_ns.expect(experience_bulk_delete)
    @experience_type_ns.doc("Delete a list of experience_type")
    def delete(self):

        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                experience = ExperienceTypeService.delete_by_uuid(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
