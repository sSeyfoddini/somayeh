import logging

from app.services.learners_service import LearnersService
from app.services.thin_client_service import StudentService
from app.util.error_handlers import InternalServerError

_log = logging.getLogger(__name__)


class LearnerService:
    @classmethod
    def insert_from_thin_client(cls, email_set):
        data_flag = False
        user_id = 1
        username = "test"

        for email in email_set:
            user = StudentService.get(email)
            if user:
                key = list(user)[0]
                user = user[key]
                data_flag = True

                learner = LearnersService.add(
                    user_id=user_id,
                    user_name=username,
                    email=email,
                    email_address_type=user.get("email_address_type",""),
                    address_type=user.get("address-type",""),
                    address1=user.get("address1",""),
                    address2=user.get("address2",""),
                    city=user.get("city",""),
                    county="",
                    state=user.get("state",""),
                    postal_code=user.get("postal_code",""),
                    effdt_addresses=user.get("effdt_addresses",""),
                    country=user.get("country",""),
                    phone_type=user.get("phone_type",""),
                    phone=user.get("phone",""),
                    country_code=user.get("country_code",""),
                    pref_phone_flag=user.get("pref_phone_flag",""),
                    birth_date=user.get("birth_date",""),
                    last_name=user.get("last_name",""),
                    first_name=user.get("first_name",""),
                    middle_initial=user.get("middle_initial",""),
                    effdt_names=user.get("effdt_names",""),
                    external_id=user.get("external_id",""),
                    otp_status=True,
                    user_consent=None,
                    consent_date=None
                )
        if not data_flag:
            raise Exception("The request does not contain valid email.")

    @classmethod
    def update_from_thin_client(cls, email_set):
        data_flag = False
        user_id = 1
        username = "test"

        for email in email_set:
            user = StudentService.get(email)
            if user:
                data_flag = True
                key = list(user)[0]
                user = user[key]

                uuid = LearnersService.get_by_email(email).uuid
                learner = LearnersService.update(
                    user_id=user_id,
                    user_name=username,
                    uuid=uuid,
                    args=user
                )
        if not data_flag:
            raise Exception("The request does not contain valid email.")
