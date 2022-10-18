import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.badgr_service import BadgrService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

badge_insert_ns = Namespace(
    "badge_get_by_mail",
    description="Badge get by mail related operations",
    decorators=[cors.crossdomain(origin="*")],
)

badge_auth_model = badge_insert_ns.model(
    "Badge_Auth",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

badge_insert_model = badge_insert_ns.model(
    "Badge_get_by_mail",
    {"email": fields.List(fields.String), "access_token": fields.String(required=True)},
)


@badge_insert_ns.route("/badge_auth")
class BadgeInsertAuth(Resource):
    def options(self):
        pass

    @badge_insert_ns.expect(badge_auth_model)
    def post(self):
        args = request.get_json()
        try:
            access_token, refresh_token = BadgrService.authanticate(args["username"], args["password"])
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                200,
                {"content-type": "application/json"},
            )

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.warning(e.__dict__)
            raise e


@badge_insert_ns.route("/badge_get_by_email")
class BadgeInsertEmail(Resource):
    def options(self):
        pass

    @badge_insert_ns.expect(badge_insert_model)
    def post(self):
        args = request.get_json()
        try:
            entityid = BadgrService.get_issusers_entityid(args["access_token"])
            asset = BadgrService.get_badge_by_email(args["access_token"], entityid, args["email"])
            return {"data": asset}, 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
