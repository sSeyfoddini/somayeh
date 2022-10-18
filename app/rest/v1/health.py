import logging

from flask import request
from flask_restx import Namespace, Resource, cors, fields

from app import db
from app.services.mail_service import MailService
from app.util.error_handlers import InternalServerError, DbConnectionError

_log = logging.getLogger(__name__)

health_database_status_ns = Namespace(
    "health",
    description="health related operations",
    decorators=[cors.crossdomain(origin="*")],
)
health_email_ns_model = health_database_status_ns.model("test email", {"email": fields.String(requied=True)})


@health_database_status_ns.route("/health")
class ConnectivityCheck(Resource):
    def options(self):
        pass

    @health_database_status_ns.doc("checking DB connection")
    def get(self):
        try:
            # to check database we will execute raw query
            db.session.execute("SELECT 1")
            return (
                {"Status": "Healthy", "DB Connection": "Available"},
                200,
                {"content-type": "application/json"},
            )
        except Exception as e:
            e = DbConnectionError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e



@health_database_status_ns.route("/email_test")
class EmailTest(Resource):
    def options(self):
        pass

    @health_database_status_ns.expect(health_email_ns_model)
    @health_database_status_ns.doc("Test email")
    def post(self):
        args = request.get_json()
        try:
            MailService.send_mail(first_name="test", last_name="test", otp="test", reciever=args["email"])

            return "Successful", 200, {"content-type": "application/json"}

        except Exception as e:
            if "status_code" not in e.__dict__:
                e = InternalServerError(str(e.args[0]))
            _log.error(e.__dict__)
            raise e
