import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.title_type_services import TitleTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

title_type_ns = Namespace(
    "title_type",
    description="TitleType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

title_type_add = title_type_ns.model(
    "TitleTypeAdd",
    {
        "name": fields.String(required=True, description="Name of title"),
        "description": fields.String(required=False, description="Description of title, if any"),
        "reference_url": fields.String(required=False, description="url for title or position"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

title_type_edit = title_type_ns.model(
    "TitleTypeEdit",
    {
        "name": fields.String(required=True, description="Name of title"),
        "description": fields.String(required=False, description="Description of title, if any"),
        "reference_url": fields.String(required=False, description="url for title or position"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@title_type_ns.route("/<string:uuid>")
class TitleTypeRest(Resource):
    def options(self):
        pass

    @title_type_ns.doc("return a TitleType")
    def get(self, uuid):
        try:
            title_type = TitleTypeService.get(uuid)
            return title_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @title_type_ns.expect(title_type_edit)
    @title_type_ns.doc("Update a TitleType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            title_type = TitleTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return title_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @title_type_ns.doc("delete a TitleType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            title_type = TitleTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return title_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@title_type_ns.route("/")
class TitleTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            title_types, total_records, page = TitleTypeService.get_all_by_filter(filter_dict)
            if title_types:
                return (
                    {
                        "data": [title_type._to_dict() for title_type in title_types],
                        "page": {"page_number": page, "records_of_page": len(title_types), "total_records": total_records},
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

    @title_type_ns.expect(title_type_add)
    @title_type_ns.doc("Create a TitleType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("title_type", args)
            title_type = TitleTypeService.add(
                user_id=user_id,
                user_name=username,
                name=args.get("name"),
                description=args.get("description"),
                reference_url=args.get("reference_url"),
                type=args.get("type"),
                external_id=args.get("external_id")
            )

            return title_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
