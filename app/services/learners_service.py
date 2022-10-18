from hashlib import sha1

from app.model.learners_model import LearnersModel
from app.persistence.learners_persistence import LearnersPersistence
from app.util.error_handlers import RecordNotFound


class LearnersService:
    @classmethod
    def add(
        cls,
        user_id,
        user_name,
        email,
        email_address_type,
        address_type,
        address1,
        address2,
        city,
        county,
        state,
        postal_code,
        effdt_addresses,
        country,
        phone_type,
        phone,
        country_code,
        pref_phone_flag,
        birth_date,
        last_name,
        first_name,
        middle_initial,
        effdt_names,
        external_id,
        otp_status,
        user_consent,
        consent_date

    ):
        learner = cls.get_by_email(email)

        if learner:
            raise Exception(f"email = {email} already exist." )

        learner = LearnersModel(
            email=sha1(email.lower().encode("utf-8")).hexdigest(),
            email_address_type=sha1(email_address_type.lower().encode("utf-8")).hexdigest() if email_address_type else None,
            address_type=sha1(address_type.lower().encode("utf-8")).hexdigest() if address_type else None,
            address1=sha1(address1.lower().encode("utf-8")).hexdigest() if address1 else None,
            address2=sha1(address2.lower().encode("utf-8")).hexdigest() if address2 else None,
            city=sha1(city.lower().encode("utf-8")).hexdigest() if city else None,
            county=sha1(county.lower().encode("utf-8")).hexdigest() if county else None,
            state=sha1(state.lower().encode("utf-8")).hexdigest() if state else None,
            postal_code=sha1(postal_code.lower().encode("utf-8")).hexdigest() if postal_code else None,
            effdt_addresses=sha1(effdt_addresses.encode("utf-8")).hexdigest() if effdt_addresses else None,
            country=sha1(country.lower().encode("utf-8")).hexdigest() if country else None,
            phone_type=sha1(phone_type.lower().encode("utf-8")).hexdigest() if phone_type else None,
            phone=sha1(phone.lower().encode("utf-8")).hexdigest() if phone else None,
            country_code=sha1(country_code.lower().encode("utf-8")).hexdigest() if country_code else None,
            pref_phone_flag=sha1(pref_phone_flag.lower().encode("utf-8")).hexdigest() if pref_phone_flag else None,
            birth_date=sha1(birth_date.encode("utf-8")).hexdigest() if birth_date else None,
            last_name=sha1(last_name.lower().encode("utf-8")).hexdigest() if last_name else None,
            first_name=sha1(first_name.lower().encode("utf-8")).hexdigest() if first_name else None,
            middle_initial=sha1(middle_initial.lower().encode("utf-8")).hexdigest() if middle_initial else None,
            effdt_names=sha1(effdt_names.encode("utf-8")).hexdigest() if effdt_names else None,
            external_id=sha1(external_id.lower().encode("utf-8")).hexdigest() if external_id else None,
            otp_status=otp_status,
            user_consent=user_consent,
            consent_date=sha1(consent_date.encode("utf-8")).hexdigest() if consent_date else None,
        )
        learner = LearnersPersistence.add(user_id, user_name, learner)
        return learner

    @classmethod
    def update(
        cls,
        user_id,
        user_name,
        uuid,
        args
    ):
        learner = LearnersPersistence.get_by_uuid(uuid)
        if learner is None:
            raise RecordNotFound("'learner' with uuid '{}' not found.".format(uuid))

        learner = LearnersModel(
            uuid=uuid,
            email=sha1(args["email"].lower().encode("utf-8")).hexdigest() if "email" in args else learner.email,
            email_address_type=sha1(args["email_address_type"].lower().encode("utf-8")).hexdigest()
                if "email_address_type" in args else learner.email_address_type,
            address_type=sha1(args["address_type"].lower().encode("utf-8")).hexdigest()
                if "address_type" in args else learner.address_type,
            address1=sha1(args["address1"].lower().encode("utf-8")).hexdigest()
                if "address1" in args else learner.address1,
            address2=sha1(args["address2"].lower().encode("utf-8")).hexdigest()
                if "address2" in args else learner.address2,
            city=sha1(args["city"].lower().encode("utf-8")).hexdigest() if "city" in args else learner.city,
            county=sha1(args["county"].lower().encode("utf-8")).hexdigest() if "county" in args else learner.county,
            state=sha1(args["state"].lower().encode("utf-8")).hexdigest() if "state" in args else learner.state,
            postal_code=sha1(args["postal_code"].lower().encode("utf-8")).hexdigest()
                if "postal_code" in args else learner.postal_code,
            effdt_addresses=sha1(args["effdt_addresses"].encode("utf-8")).hexdigest()
                if "effdt_addresses" in args else learner.effdt_addresses,
            country=sha1(args["country"].lower().encode("utf-8")).hexdigest()
                if "country" in args else learner.country,
            phone_type=sha1(args["phone_type"].lower().encode("utf-8")).hexdigest()
                if "phone_type" in args else learner.phone_type,
            phone=sha1(args["phone"].lower().encode("utf-8")).hexdigest() if "phone" in args else learner.phone,
            country_code=sha1(args["country_code"].lower().encode("utf-8")).hexdigest()
                if "country_code" in args else learner.country_code,
            pref_phone_flag=sha1(args["pref_phone_flag"].lower().encode("utf-8")).hexdigest()
                if "pref_phone_flag" in args else learner.pref_phone_flag,
            birth_date=sha1(args["birth_date"].encode("utf-8")).hexdigest()
                if "birth_date" in args else learner.birth_date,
            last_name=sha1(args["last_name"].lower().encode("utf-8")).hexdigest()
                if "last_name" in args else learner.last_name,
            first_name=sha1(args["first_name"].lower().encode("utf-8")).hexdigest()
                if "first_name" in args else learner.first_name,
            middle_initial=sha1(args["middle_initial"].lower().encode("utf-8")).hexdigest()
                if "middle_initial" in args else learner.middle_initial,
            effdt_names=sha1(args["effdt_names"].encode("utf-8")).hexdigest()
                if "effdt_names" in args else learner.effdt_names,
            external_id=sha1(args["external_id"].lower().encode("utf-8")).hexdigest()
                if "external_id" in args else learner.external_id,
            otp_status=args["otp_status"] if "otp_status" in args else learner.otp_status,
            user_consent=args["user_consent"] if "user_consent" in args else learner.user_consent,
            consent_date=sha1(args["consent_date"].encode("utf-8")).hexdigest()
                if "consent_date" in args else learner.consent_date,
        )
        learner = LearnersPersistence.update(user_id, user_name, learner)

        return learner

    @classmethod
    def delete_all(cls):
        LearnersPersistence.delete_all()

    @classmethod
    def delete_by_uuid(cls, user_id, user_name, uuid):
        learner = LearnersPersistence.get_by_uuid(uuid)
        if learner is None:
            raise RecordNotFound("'learner' with uuid '{}' not found.".format(uuid))
        LearnersPersistence.delete(user_id, user_name, learner)
        return learner

    @classmethod
    def get_by_email(cls, email):
        email = sha1(email.lower().encode("utf-8")).hexdigest()
        learner = LearnersPersistence.get_by_email(email)
        return learner

    @classmethod
    def get_by_uuid(cls, uuid):
        learner = LearnersPersistence.get_by_uuid(uuid)
        if learner is None:
            raise RecordNotFound("'learner' with uuid '{}' not found.".format(uuid))
        return learner

    @classmethod
    def get_all(cls):
        return LearnersPersistence.get_all()

    @classmethod
    def get_all_by_filter(cls, filter_dict):
        for key, val in filter_dict.items():
            if key not in ["user_consent","otp_status","sort","page","limit","uuid"]:
                filter_dict[key] = sha1(val.lower().encode("utf-8")).hexdigest()
        print(filter_dict)
        return LearnersPersistence.get_all_by_filter(filter_dict)

    @classmethod
    def update_consent(cls,user_id, user_name, consent, email):
        old_learner = cls.get_by_email(email)
        if old_learner is None:
            raise RecordNotFound("'learner' with email '{}' not found.".format(email))
        learner = LearnersModel(
            uuid=old_learner.uuid,
            email=old_learner.email,
            email_address_type=old_learner.email_address_type,
            address_type=old_learner.address_type,
            address1=old_learner.address1,
            address2=old_learner.address2,
            city=old_learner.city,
            county=old_learner.county,
            state=old_learner.state,
            postal_code=old_learner.postal_code,
            effdt_addresses=old_learner.effdt_addresses,
            country=old_learner.country,
            phone_type=old_learner.phone_type,
            phone=old_learner.phone,
            country_code=old_learner.country_code,
            pref_phone_flag=old_learner.pref_phone_flag,
            birth_date=old_learner.birth_date,
            last_name=old_learner.last_name,
            first_name=old_learner.first_name,
            middle_initial=old_learner.middle_initial,
            effdt_names=old_learner.effdt_names,
            external_id=old_learner.external_id,
            otp_status=old_learner.otp_status,
            user_consent=consent,
            consent_date=old_learner.consent_date,
        )
        learner = LearnersPersistence.update(user_id, user_name, learner)

        return learner
