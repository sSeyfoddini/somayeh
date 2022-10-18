import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.thin_client_service import OrgLocationService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
ps_org_location_ns = Namespace(
    "ps_org_location",
    description="ps_org_location related operations",
    decorators=[cors.crossdomain(origin="*")],
)

org = ps_org_location_ns.model(
    "org_location", {"ext_org_id": fields.String(required=True), "org_location": fields.String(required=True)}
)
org_location_model = ps_org_location_ns.model(
    "org_location", {"data": fields.List(fields.Nested(org)), "max_date": fields.Integer(required=True)}
)


@ps_org_location_ns.route("/ps_org_location")
class OrgLocation(Resource):
    def options(self):
        pass

    @ps_org_location_ns.expect(org_location_model)
    @ps_org_location_ns.doc("fetch org location data")
    def get(self):
        args = request.get_json()
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            org_data = OrgLocationService.get(args, page, limit)
            if org_data:
                return org_data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
