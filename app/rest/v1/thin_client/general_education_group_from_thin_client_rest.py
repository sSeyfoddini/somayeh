import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import GeneralEducationGroupService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
ps_general_ns = Namespace(
    "ps_general_education_group",
    description="general education group related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@ps_general_ns.route("/ps_general_education_group")
class GeneralGet(Resource):
    def options(self):
        pass

    @ps_general_ns.doc("get all general education group data")
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            data = GeneralEducationGroupService.get(page, limit)
            if data:
                return data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}

        except Exception as e:

            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))

            _log.error(e.__dict__)

            raise e
