from uuid import uuid4
from app import db

def uuid():
    return str(uuid4())


class LearnersModel(db.Model):
    """
    Data model for learners DB table.
    """

    __tablename__ = "learners"
    uuid = db.Column(db.String, primary_key=True, default=uuid)
    email = db.Column(db.String, nullable=False)
    email_address_type = db.Column(db.String, nullable=True)
    address_type = db.Column(db.String, nullable=True)
    address1 = db.Column(db.String, nullable=True)
    address2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    county = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String, nullable=True)
    effdt_addresses = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    phone_type = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    country_code = db.Column(db.String, nullable=True)
    pref_phone_flag = db.Column(db.String, nullable=True)
    birth_date = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    middle_initial = db.Column(db.String, nullable=True)
    effdt_names = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)
    otp_status = db.Column(db.Boolean, nullable=False)
    user_consent = db.Column(db.Boolean, nullable=True)
    consent_date = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "email": self.email,
            "email_address_type": self.email_address_type,
            "address_type": self.address_type,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "county": self.county,
            "state": self.state,
            "postal_code": self.postal_code,
            "effdt_addresses": self.effdt_addresses,
            "country": self.country,
            "phone_type": self.phone_type,
            "phone": self.phone,
            "country_code": self.country_code,
            "pref_phone_flag": self.pref_phone_flag,
            "birth_date": self.birth_date,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "middle_initial": self.middle_initial,
            "effdt_names": self.effdt_names,
            "external_id": self.external_id,
            "otp_status": str(self.otp_status),
            "user_consent": str(self.user_consent),
            "consent_date": self.consent_date,
        }

    def _clone(self):
        return LearnersModel(
            uuid=self.uuid,
            email=self.email,
            email_address_type=self.email_address_type,
            address_type=self.address_type,
            address1=self.address1,
            address2=self.address2,
            city=self.city,
            county=self.county,
            state=self.state,
            postal_code=self.postal_code,
            effdt_addresses=self.effdt_addresses,
            country=self.country,
            phone_type=self.phone_type,
            phone=self.phone,
            country_code=self.country_code,
            pref_phone_flag=self.pref_phone_flag,
            birth_date=self.birth_date,
            last_name=self.last_name,
            first_name=self.first_name,
            middle_initial=self.middle_initial,
            effdt_names=self.effdt_names,
            external_id=self.external_id,
            otp_status=self.otp_status,
            user_consent=self.user_consent,
            consent_date=self.consent_date,
        )
