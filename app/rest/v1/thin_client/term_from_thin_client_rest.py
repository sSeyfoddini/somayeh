import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.services.thin_client_service import TermService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)
term_ns = Namespace(
    "term",
    description="term related operations",
    decorators=[cors.crossdomain(origin="*")],
)


@term_ns.route("/term")
class TermGet(Resource):
    def options(self):
        pass

    @term_ns.doc("get all term data")
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        try:
            term_data = TermService.get(page, limit)
            if term_data:
                return term_data, 200, {"content-type": "application/json"}
            else:
                return {"massage": "No content"}, 204, {"content-type": "application/json"}


        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
