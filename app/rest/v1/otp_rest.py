import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app.services.otp_service import OtpService
from app.util.check_field import CheckField
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)

otp_ns = Namespace(
    "otp",
    description="Otp related operations",
    decorators=[cors.crossdomain(origin="*")],
)

otp_add = otp_ns.model(
    "OtpAdd",
    {"email": fields.String(requied=True), "otp": fields.Integer(required=True)},
)

otp_edit = otp_ns.model(
    "OtpEdit",
    {"email": fields.String(requied=True), "otp": fields.Integer(required=True)},
)


@otp_ns.route("/<string:uuid>")
class OtpRest(Resource):
    def options(self):
        pass

    @otp_ns.doc("return a Otp")
    def get(self, uuid):
        try:
            otp = OtpService.get(uuid)
            return otp._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @otp_ns.expect(otp_edit)
    @otp_ns.doc("Update a Otp")
    def put(self, uuid):
        args = request.get_json()
        # todo should take the user_id and username from token
        try:
            # todo should check the permission here
            otp = OtpService.update(
                email=args["email"],
                otp=args["otp"],
            )
            return otp._to_dict(), 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e

    @otp_ns.doc("delete a Otp")
    def delete(self, uuid):
        # todo should take the user_id and username from token
        # todo should check the permission here
        try:
            otp = OtpService.delete(uuid=uuid)
            return otp._to_dict(), 204, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e


@otp_ns.route("/")
class OtpListRest(Resource):
    def options(self):
        pass

    def get(self):
        filter_dict = request.args.to_dict()
        try:
            otps, total_records, page = OtpService.get_all_by_filter(filter_dict)
            if otps:
                return (
                    {
                        "data": [otp._to_dict() for otp in otps],
                        "page": {"page_number": page, "records_of_page": len(otps), "total_records": total_records},
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

    @otp_ns.expect(otp_add)
    @otp_ns.doc("Create a Otp")
    def post(self):
        args = request.get_json()

        try:
            CheckField.check_missing_field_and_field_type("otp", args)
            
            otp = OtpService.add(email=args["email"], otp=args["otp"])

            return otp._to_dict(), 200, {"content-type": "application/json"}
        
        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
        
