import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.pocket_user_credentials_services.title_services import TitleService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

title_ns = Namespace(
    "title",
    description="Title related operations",
    decorators=[cors.crossdomain(origin="*")],
)

title_add = title_ns.model(
    "TitleAdd",
    {
        "credential_type_id": fields.String(required=True, description="type of credential, always id for title"),
        "credential_type_label": fields.String(required=True, description='Always "title"'),
        "title_type_id": fields.Integer(required=True, description="id of the title"),
        "title_type_label": fields.String(required=True, description="Name of title"),
        "organization_id": fields.Integer(required=True, description="Organization DID"),
        "organization_label": fields.String(required=True, description="Name of organization"),
        "conferral_date": fields.Date(required=True, description="Date title was conferred"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

title_edit = title_ns.model(
    "TitleEdit",
    {
        "credential_type_id": fields.String(required=True, description="type of credential, always id for title"),
        "credential_type_label": fields.String(required=True, description='Always "title"'),
        "title_type_id": fields.Integer(required=True, description="id of the title"),
        "title_type_label": fields.String(required=True, description="Name of title"),
        "organization_id": fields.Integer(required=True, description="Organization DID"),
        "organization_label": fields.String(required=True, description="Name of organization"),
        "conferral_date": fields.Date(required=True, description="Date title was conferred"),
        "type": fields.String(required=False),
        "external_id": fields.String(required=True),
    },
)

title_bulk_delete = title_ns.model("TitleBulkDelete", {"uuid": fields.List(fields.String(required=True))})


@title_ns.route("/<string:uuid>")
class TitleRest(Resource):
    def options(self):
        pass

    @title_ns.doc("return a Title")
    def get(self, uuid):
        try:
            title = TitleService.get(uuid)
            return title._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @title_ns.expect(title_edit)
    @title_ns.doc("Update a Title")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        user_id = 1
        username = "test"

        try:
            # todo should check the permission here
            title = TitleService.update(
                user_id=user_id,
                user_name=username,
                uuid=uuid,
                args=args
            )
            return title._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @title_ns.doc("delete a Title")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        user_id = 1
        username = "test"

        try:
            title = TitleService.delete(user_id=user_id, user_name=username, uuid=uuid)
            return title._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@title_ns.route("/")
class TitleListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            titles, total_records, page = TitleService.get_all_by_filter(filter_dict)
            if titles:
                return (
                    {
                        "data": [title._to_dict() for title in titles],
                        "page": {"page_number": page, "records_of_page": len(titles), "total_records": total_records},
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

    @title_ns.expect(title_add)
    @title_ns.doc("Create a Title")
    def post(self):
        args = request.get_json()

        user_id = 1
        username = "test"
        try:
            CheckField.check_missing_field_and_field_type("title", args)
            title = TitleService.add(
                user_id=user_id,
                user_name=username,
                credential_type_id=args.get("credential_type_id"),
                credential_type_label=args.get("credential_type_label"),
                title_type_id=args.get("title_type_id"),
                title_type_label=args.get("title_type_label"),
                organization_id=args.get("organization_id"),
                organization_label=args.get("organization_label"),
                conferral_date=args.get("conferral_date"),
                type=args.get("type"),
                external_id=args.get("external_id"),
            )

            return title._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    def delete(self):
        try:
            TitleService.delete_all()
            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

@title_ns.route("/bulk_delete")
class TitleBulkDeleteRest(Resource):
    def options(self):
        pass

    @title_ns.expect(title_bulk_delete)
    @title_ns.doc("Delete a list of title")
    def delete(self):
        args = request.get_json()
        user_id = 1
        username = "test"
        try:
            for uuid in args["uuid"]:
                title = TitleService.delete(user_id, username, uuid)

            return "Successful", 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
