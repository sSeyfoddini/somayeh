import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.skill_portfolio_endorsement_services.mime_type_service import MimeTypeService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

mime_type_ns = Namespace(
    "mime_type",
    description="MimeType related operations",
    decorators=[cors.crossdomain(origin="*")],
)

mime_type_add = mime_type_ns.model(
    "MimeTypeAdd",
    {
        "mime_type1": fields.String(required=True),
        "extension": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

mime_type_edit = mime_type_ns.model(
    "MimeTypeEdit",
    {
        "mime_type1": fields.String(required=True),
        "extension": fields.String(required=True),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)


@mime_type_ns.route("/<string:uuid>")
class MimeTypeRest(Resource):
    def options(self):
        pass

    @mime_type_ns.doc("return a MimeType")
    def get(self, uuid):
        try:
            mime_type = MimeTypeService.get(uuid)
            return mime_type._to_dict(), 200, {"content-type": "application/json"}
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @mime_type_ns.expect(mime_type_edit)
    @mime_type_ns.doc("Update a MimeType")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            mime_type = MimeTypeService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return mime_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @mime_type_ns.doc("delete a MimeType")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            mime_type = MimeTypeService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return mime_type._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@mime_type_ns.route("/")
class MimeTypeListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            mime_types, total_records, page = MimeTypeService.get_all_by_filter(filter_dict)
            if mime_types:
                return (
                    {
                        "data": [mime_type._to_dict() for mime_type in mime_types],
                        "page": {"page_number": page, "records_of_page": len(mime_types), "total_records": total_records},
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

    @mime_type_ns.expect(mime_type_add)
    @mime_type_ns.doc("Create a MimeType")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("mime_type",args)
            mime_type = MimeTypeService.add(
                user_id=user_id,
                user_name=username,
                mime_type1=args.get("mime_type1"),
                extension=args.get("extension"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return mime_type._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
