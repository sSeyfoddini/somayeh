import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import RolesService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
ps_roles_ns = Namespace(
    "ps_roles",
    description="roles related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@ps_roles_ns.route("/ps_roles")
class RolesGet(Resource):
    def options(self):
        pass

    @ps_roles_ns.doc("get all roles data")
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            data = RolesService.get(page, limit)
            if data:
                return data, 200, {"content-type": "application/json"}

            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
