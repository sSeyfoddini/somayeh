# import asyncio
# import logging
# import os
# import uuid
#
# import requests
# from aiohttp import web
# from strata.service import (
#     badge_service,
#     class_completion_services,
#     class_enrollment_services,
#     college_affiliation_service,
#     program_affiliation_service,
#     skill_service,
#     student_affiliation_service,
#     user_info_service,
# )
# from strata.service.message_service import message_services
#
#
# class MessageObj:
#     def __init__(self, data_dict: dict):
#         self.connection_external_id = data_dict["connection_external_id"]
#         self.connection_id = data_dict["connection_id"]
#         self.message_body = MessageBody(data_dict["message_body"])
#
#
# class MessageBody:
#     def __init__(self, data_dict: dict):
#         self.type = data_dict["type"]
#         self.key = data_dict["key"]
#         self.email = data_dict["email"]
#         if "code" in data_dict:
#             self.code = data_dict["code"]
#
#
# class EmailOtpVerification:
#     def options(self):
#     pass
#
#     def get_routes(self):
#         return [
#             web.post("/email-otp-verification", self._message_body),
#         ]
#
#     def _convert(self, data: dict) -> MessageObj:
#         return MessageObj(data)
#
#     async def _email_validation(self, message_object: MessageObj):
#         user = await user_info_service.get_by_email(message_object.message_body.email)
#         message_id = str(uuid.uuid4())
#         response = {
#             "connection_external_id": "",
#             "connection_id": message_object.connection_id,
#             "body": {
#                 "type": message_object.message_body.type,
#                 "key": message_object.message_body.key,
#                 "email": message_object.message_body.email,
#                 "status": False,
#             },
#             "external_id": message_id,
#         }
#
#         if user:
#             response["body"]["status"] = True
#         message_services.send_message(response)
#
#     async def _otp_validation(self, message_object: MessageObj):
#         code = 111111
#         message_id = str(uuid.uuid4())
#         response = {
#             "connection_external_id": "",
#             "connection_id": message_object.connection_id,
#             "body": {
#                 "type": message_object.message_body.type,
#                 "key": message_object.message_body.key,
#                 "email": message_object.message_body.email,
#                 "status": False,
#             },
#             "external_id": message_id,
#         }
#         if message_object.message_body.code and code == int(message_object.message_body.code):
#             response["body"]["status"] = True
#         message_services.send_message(response)
#         return response["body"]["status"]
#
#     async def _message_body(self, request):
#
#         logging.debug(f"Received request on message endpoint")
#         body = await request.json()  # get from user api888888888888888
#         logging.debug(f"Request message: {body}")
#
#         message_object = self._convert(body)
#
#         valid = False
#         if message_object.message_body.type == "email-validation":
#             await self._email_validation(message_object)
#
#         elif message_object.message_body.type == "otp-verification":
#             valid = await self._otp_validation(message_object)
#
#         if valid:
#             message_id = str(uuid.uuid4())
#             user = await user_info_service.get_by_email(message_object.message_body.email)
#             pocket_core_api_set_external_id = config.pocket_core_base_url + "/connection/set_external_id"
#             external_id = user.external_id
#             requests.put(
#                 pocket_core_api_set_external_id,
#                 json={"connection_id": message_object.connection_id, "external_id": external_id},
#             )
#
#             await user_info_service.issue_identity(external_id)
#
#             loop = asyncio.get_event_loop()
#             loop.create_task(self._issue_rest(external_id))
#
#         return web.json_response({"status": "success"})
#
#     async def _issue_rest(self, external_id: str):
#         await asyncio.sleep(5)
#         await class_completion_services.issue_class_completion(external_id)
#         await class_enrollment_services.issue_class_enrollment(external_id)
#         await skill_service.issue_skill(external_id)
#         await badge_service.issue_badge(external_id)
#         await student_affiliation_service.issue(external_id)
#         await college_affiliation_service.issue(external_id)
#         await program_affiliation_service.issue(external_id)
#
#
# email_otp_verification_api = EmailOtpVerification()
