import logging

import requests
from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.util.error_handlers import InternalServerError


class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}


_log = logging.getLogger(__name__)

api_connection_ns = Namespace(
    "api_connection",
    description="",
    decorators=[cors.crossdomain(origin="*")],
)

api_connection_add = api_connection_ns.model(
    "APIConnectionAdd",
    {
        "external_id": fields.String(required=True),
        "additional_data": DictItem(attribute="additional_data"),
    },
)


@api_connection_ns.route("/post_connection")
class APIConnectionListRest(Resource):
    def options(self):
        pass

    @api_connection_ns.expect(api_connection_add)
    @api_connection_ns.doc("/Create a connection identified by external id ")
    def post(self):
        try:
            args = request.get_json()
            url = "https://pocket-vscc-dev-ec2.getpocket.io:33333/connection"

            post_data = {
                "external_id": args["external_id"],
                "additional_data": args["additional_data"],
            }
            response = requests.post(url, json=post_data, timeout=5)
            response_content = response.json()

            return (
                response_content,
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
