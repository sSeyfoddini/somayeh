import logging

from flask import request
from flask_restx import Namespace, Resource, cors

from app.model.core_integration.message_model import MessageRequest
from app.services.core_integration.message_service import MessageService

_log = logging.getLogger(__name__)

message_ns = Namespace(
    "core",
    description="Message sender/receiver to/from core",
    decorators=[cors.crossdomain(origin="*")],
)


@message_ns.route("/message")
class MessageRest(Resource):
    def _convert(self, message_request) -> MessageRequest:
        return MessageRequest(message_request)

    def options(self):
        pass

    @message_ns.doc("receive a message")
    def post(self):
        _log.info(f"Received request on message endpoint")
        try:
            message_request = request.get_json()
        except Exception as e:
            _log.debug(f"Error is: {e}")
            raise
        _log.info(f"Request message: {message_request}")
        message_request = self._convert(message_request)

        if message_request.message_body.type == "email-validation":
            email_validation = MessageService.email_validation(message_request)
            if email_validation:
                return {"message": "Successful"}, 200, {"content-type": "application/json"}
            return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        if message_request.message_body.type == "register":
            email_validation = MessageService.register(message_request)
            if email_validation:
                return {"message": "Successful"}, 200, {"content-type": "application/json"}
            return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        elif message_request.message_body.type == "otp-verification":
            otp_validation = MessageService.otp_validation(message_request)
            if otp_validation:
                return {"message": "Successful"}, 200, {"content-type": "application/json"}
            return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        elif message_request.message_body.type == "request-badge":
            request_badge = MessageService.request_badge(message_request)
            if request_badge:
                return {"message": "Successful"}, 200, {"content-type": "application/json"}
            return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        elif message_request.message_body.type == "get-all-badges":
            request_badge = MessageService.get_all_badges(message_request)
            if request_badge:
                return {"message": "Successful"}, 200, {"content-type": "application/json"}
            return {"message": "Unsuccessful"}, 500, {"content-type": "application/json"}

        return {"message": "Not valid message operation!"}, 500, {"content-type": "application/json"}
