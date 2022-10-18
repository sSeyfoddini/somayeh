import datetime
import logging
import uuid
from random import randint

import requests

from app.config import Config
from app.model.core_integration.badge_model import BadgeModel
from app.model.core_integration.message_model import MessageRequest
from app.model.core_integration.user_identity_model import UserIdentitySchemaModel
from app.persistence.learners_persistence import LearnersPersistence
from app.services.badgr_service import BadgrService
from app.services.core_integration.issue_badge import IssueBadge
from app.services.core_integration.issue_user_identity import IssueUserIdentity
from app.services.core_integration.set_external_id import SetExternalId
from app.services.credential_schema_tables_services.badge_service import BadgeService
from app.services.credential_schema_tables_services.badge_type_service import BadgeTypeService
from app.services.credential_schema_tables_services.credential_type_service import CredentialTypeService
from app.services.mail_service import MailService
from app.services.otp_service import OtpService
from app.services.thin_client_service import StudentService
from app.services.learners_service import LearnersService

_log = logging.getLogger(__name__)


class MessageService:
    @classmethod
    def _send_message(cls, message):
        _log.info(f"Sending Message to the Core with url:{Config.pocket_core_api_message}, and message:{message}")
        print(f"Sending Message to the Core with url:{Config.pocket_core_api_message}, and message:{message}")
        response = requests.post(Config.pocket_core_api_message, json=message)
        status_code = response.status_code
        print(response.text)
        _log.info(f"Core response:{status_code}")
        if status_code == 200:
            return True
        return False

    @classmethod
    def email_validation(cls, message_request: MessageRequest):
        _log.info(f"Validation message received with email: {message_request.message_body.email}")
        user = StudentService.get(message_request.message_body.email)
        message_id = str(uuid.uuid4())
        response = {
            "connection_external_id": "",
            "connection_id": message_request.connection_id,
            "body": {
                "type": message_request.message_body.type,
                "key": message_request.message_body.key,
                "email": message_request.message_body.email,
                "consent_acceptance": message_request.message_body.consent_acceptance,
                "status": False,
            },
            "external_id": message_id,
        }
        if user:
            _log.info(f"User found for validation message with email: {message_request.message_body.email}")
            key = list(user)[0]
            user = user[key]
            response["body"]["status"] = True
            _log.info(f"User availability: {response['body']['status']}")
            otp = randint(100000, 999999)
            OtpService.update(message_request.message_body.email, otp)
            MailService.send_mail(
                first_name=user["first_name"],
                last_name=user["last_name"],
                otp=otp,
                reciever=message_request.message_body.email,
            )
        if not LearnersService.get_by_email(message_request.message_body.email) and user:
            user_id = 1
            LearnersService.add(
                user_id=user_id,
                user_name=message_request.message_body.email,
                email=message_request.message_body.email,
                email_address_type=user["email_address_type"] if "email_address_type" in user else "",
                address_type=user["address-type"] if "address-type" in user else "",
                address1=user["address1"] if "address1" in user else "",
                address2=user["address2"] if "address2" in user else "",
                city=user["city"] if "city" in user else "",
                county=user["country"] if "country" in user else "",
                state=user["state"] if "state" in user else "",
                postal_code=user["postal_code"] if "postal_code" in user else "",
                effdt_addresses=user["effdt_addresses"] if "effdt_addresses" in user else "",
                country=user["country"] if "country" in user else "",
                phone_type=user["phone_type"] if "phone_type" in user else "",
                phone=user["phone"] if "phone" in user else "",
                country_code=user["country_code"] if "country_code" in user else "",
                pref_phone_flag=user["pref_phone_flag"] if "pref_phone_flag" in user else False,
                birth_date=user["birth_date"],
                last_name=user["last_name"],
                first_name=user["first_name"],
                middle_initial=user["middle_initial"] if "middle_initial" in user else "",
                effdt_names=user["effdt_names"] if "effdt_names" in user else None,
                external_id=user["external_id"],
                otp_status=False,
                user_consent=True,
                consent_date=str(datetime.datetime.now()),
            )
        _log.info(f"User not found for validation message with email: {message_request.message_body.email}")
        send_message_status = cls._send_message(response)
        _log.info(f"Core message send status: {send_message_status}")
        return send_message_status and response["body"]["status"]

    @classmethod
    def register(cls, message_request: MessageRequest):
        _log.info(f"Register message received with email: {message_request.message_body.email}")
        user = StudentService.get(message_request.message_body.email)
        message_id = str(uuid.uuid4())
        response = {
            "connection_external_id": "",
            "connection_id": message_request.connection_id,
            "body": {
                "type": message_request.message_body.type,
                "key": message_request.message_body.key,
                "email": message_request.message_body.email,
                "consent_acceptance": message_request.message_body.consent_acceptance,
                "status": True,

            },
            "external_id": message_id,
        }
        if not LearnersService.get_by_email(message_request.message_body.email):
            user_id = 1
            LearnersService.add(
                user_id=user_id,
                user_name=message_request.message_body.email,
                email=message_request.message_body.email,
                email_address_type=user["email_address_type"] if user and "email_address_type" in user else "",
                address_type=user["address-type"] if user and "address-type" in user else "",
                address1=user["address1"] if user and "address1" in user else "",
                address2=user["address2"] if user and "address2" in user else "",
                city=user["city"] if user and "city" in user else "",
                county=user["country"] if user and "country" in user else "",
                state=user["state"] if user and "state" in user else "",
                postal_code=user["postal_code"] if user and "postal_code" in user else "",
                effdt_addresses=user["effdt_addresses"] if user and "effdt_addresses" in user else "",
                country=user["country"] if user and "country" in user else "",
                phone_type=user["phone_type"] if user and "phone_type" in user else "",
                phone=user["phone"] if user and "phone" in user else "",
                country_code=user["country_code"] if user and "country_code" in user else "",
                pref_phone_flag=user["pref_phone_flag"] if user and "pref_phone_flag" in user else False,
                birth_date=user["birth_date"] if user and "birth_date" in user else None,
                last_name=user["last_name"] if user and "last_name" in user else message_request.message_body.last_name,
                first_name=user[
                    "first_name"] if user and "first_name" in user else message_request.message_body.first_name,
                middle_initial=user["middle_initial"] if user and "middle_initial" in user else "",
                effdt_names=user["effdt_names"] if user and "effdt_names" in user else None,
                external_id=user["external_id"] if user and "external_id" in user else None,
                otp_status=False,
                user_consent=True,
                consent_date=str(datetime.datetime.now()),
            )
        if user:
            key = list(user)[0]
            user = user[key]
        _log.info(f"User found for validation message with email: {message_request.message_body.email}")
        otp = randint(100000, 999999)
        OtpService.update(message_request.message_body.email, otp)
        MailService.send_mail(
            first_name=user["first_name"] if user else message_request.message_body.first_name,
            last_name=user["last_name"] if user else message_request.message_body.last_name,
            otp=otp,
            reciever=message_request.message_body.email,
        )

        _log.info(f"User not found for validation message with email: {message_request.message_body.email}")
        send_message_status = cls._send_message(response)
        _log.info(f"Core message send status: {send_message_status}")
        return send_message_status

    @classmethod
    def otp_validation(cls, message_request: MessageRequest):
        _log.info(f"Otp_validation message with email: {message_request.message_body.email}")
        print(f"Otp_validation message with email: {message_request.message_body.email}")
        issue_user_identity_status = False
        message_id = str(uuid.uuid4())
        response = {
            "connection_external_id": "",
            "connection_id": message_request.connection_id,
            "body": {
                "type": message_request.message_body.type,
                "key": message_request.message_body.key,
                "email": message_request.message_body.email,
                "status": False,
            },
            "external_id": message_id,
        }
        code = None
        data = OtpService.get_by_mail(message_request.message_body.email)
        learner_data = LearnersService.get_by_email(message_request.message_body.email)
        if data:
            code = data.otp
        if message_request.message_body.code and int(code) == int(message_request.message_body.code):
            response["body"]["status"] = True
        send_message_status = cls._send_message(response)
        badge_status = False
        if send_message_status and response["body"]["status"] and learner_data:
            print("OTP Validation Success")
            user = StudentService.get(message_request.message_body.email)
            if user:
                key = list(user)[0]
                user = user[key]

            learner_data.otp_status = True
            LearnersPersistence.update(learner_data.uuid, learner_data.email, learner_data)
            external_id = learner_data.uuid
            SetExternalId.set_external_id(message_request.connection_id, external_id)
            user_identity = UserIdentitySchemaModel(
                user["first_name"] if user else message_request.message_body.first_name,
                user["last_name"] if user else message_request.message_body.last_name,
                user["external_id"] if user else None, user["birth_date"] if user else None,
                message_request.message_body.email)
            issue_user_identity_status = IssueUserIdentity.issue_identity(user_identity, external_id)

            user_id = 1
            username = "test"
            BadgeTypeService.insert_all_from_badgr(user_id=user_id, username=username)
            badge_types, _, _ = BadgeTypeService.get_all_by_filter(
                {"auto_issue": True, "extrernal_partner_label": "badgr"})
            access_token, refresh_token = BadgrService.authanticate(Config.BADGER_USERNAME, Config.BADGER_PASSWORD)

            credential_type_label = "general_education_group_asu"
            credential_type, total_records, page = CredentialTypeService.get_all_by_filter(
                {"name": credential_type_label})
            credential_type_id = credential_type[0].uuid
            for badge_type in badge_types:
                print("Active badge_type found")

                badge, _, _ = BadgeService.get_all_by_filter(
                    {"badge_type_uuid": badge_type.uuid, "learner_uuid": learner_data.uuid})
                print(f"badge_type_uuid:{badge_type.uuid}, learner_uuid:{learner_data.uuid}, badge:{badge}")
                if badge is None or len(badge) == 0:
                    print("Insert to badge table")
                    data = BadgrService.insert_in_badgr(eval(badge_type.json), message_request.message_body.email,
                                                        access_token)
                    badge = BadgeService.add(
                        user_id=user_id,
                        user_name=username,
                        credential_type_id=credential_type_id,
                        credential_type_label=credential_type_label,
                        class_id=data["badgeclass"],
                        external_user_id="",
                        badge_type_uuid=badge_type.uuid,
                        badge_name=badge_type.name,
                        badge_description="",
                        badge_org_id="67abcf62-0be9-4204-8822-325992f6857b",
                        badge_org_label="ASU",
                        badge_org_logo="",
                        badge_date="",
                        badge_external_link=data["openBadgeId"],
                        badge_json={},
                        key="",
                        learner_uuid=learner_data.uuid
                    )
                    issue_badge = BadgeModel(badge.uuid, badge.badge_name, str(datetime.datetime.now()),
                                             badge.badge_description
                                             , badge.badge_image, badge.badge_external_link)
                    badge_status = IssueBadge.issue_badge(learner_data.uuid, issue_badge)

        status = all(
            [
                send_message_status,
                response["body"]["status"],
                issue_user_identity_status,
                badge_status
            ]
        )
        return status

    @classmethod
    def request_badge(cls, message_request: MessageRequest):
        _log.info(f"Request_badge message with email: {message_request.message_body.email}")
        print(f"Request_badge message with email: {message_request.message_body.email}")

        badge_data = BadgeService.get(message_request.message_body.badge_id)
        issue_badge = BadgeModel(badge_data.uuid, badge_data.badge_name, str(datetime.datetime.now()),
                                 badge_data.badge_description
                                 , badge_data.badge_image, badge_data.badge_external_link)
        learner = LearnersService.get_by_email(message_request.message_body.email)
        status = IssueBadge.issue_badge(learner.uuid, issue_badge)
        return status

    @classmethod
    def get_all_badges(cls, message_request: MessageRequest):
        _log.info(f"Request_get all badges message with email: {message_request.message_body.email}")
        print(f"Request_get all badges message with email: {message_request.message_body.email}")
        message_id = str(uuid.uuid4())

        learner = LearnersService.get_by_email(message_request.message_body.email)
        badge_data = []
        if learner:
            badge_data = BadgeService.get_all_by_filter({"learner_uuid": learner.uuid}, True)[0]

        response = {
            "connection_external_id": "",
            "connection_id": message_request.connection_id,
            "body": {
                "type": message_request.message_body.type,
                "key": message_request.message_body.key,
                "email": message_request.message_body.email,
                "uuids": badge_data,
            },
            "external_id": message_id,
        }
        send_message_status = cls._send_message(response)

        return send_message_status
