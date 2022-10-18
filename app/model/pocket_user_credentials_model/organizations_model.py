from uuid import uuid4

from app import db


def uuid():
    return str(uuid4())


class OrganizationsModel(db.Model):
    """
    Data model for Organizations DB table.
    """

    __tablename__ = "organizations"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    abbreviation = db.Column(db.String, nullable=True)
    type_id = db.Column(db.String, nullable=False, index=True)
    type_name = db.Column(db.String, nullable=True, index=True)
    subtype_id = db.Column(db.String, nullable=True, index=True)
    organization_subtype_name = db.Column(db.String, nullable=True)
    parent_id = db.Column(db.String, nullable=True, index=True)
    parent_name = db.Column(db.String, nullable=True, index=True)
    reference_url = db.Column(db.String, nullable=True)
    logo = db.Column(db.JSON, nullable=True)
    background = db.Column(db.JSON, nullable=True)
    mail = db.Column(db.String, nullable=True)
    street_1 = db.Column(db.String, nullable=False)
    street_2 = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    external_id = db.Column(db.String, nullable=True)
    external_name = db.Column(db.String, nullable=True)
    badgr_entityID = db.Column(db.String, nullable=True)
    issuer_id = db.Column(db.String, nullable=True)


    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "abbreviation": self.abbreviation,
            "type_id": self.type_id,
            "type_name": self.type_name,
            "subtype_id": self.subtype_id,
            "parent_id": self.parent_id,
            "parent_name": self.parent_name,
            "reference_url": self.reference_url,
            "logo": self.logo,
            "background": self.background,
            "mail": self.mail,
            "street_1": self.street_1,
            "street_2": self.street_2,
            "country": self.country,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code,
            "external_id": self.external_id,
            "external_name": self.external_name,
            "badgr_entityID": self.badgr_entityID,
            "issuer_id": self.issuer_id
        }

    def _clone(self):
        return OrganizationsModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            abbreviation=self.abbreviation,
            type_id=self.type_id,
            type_name=self.type_name,
            subtype_id=self.subtype_id,
            parent_id=self.parent_id,
            parent_name=self.parent_name,
            reference_url=self.reference_url,
            logo=self.logo,
            background=self.background,
            mail=self.mail,
            street_1=self.street_1,
            street_2=self.street_2,
            country=self.country,
            city=self.city,
            region=self.region,
            postal_code=self.postal_code,
            external_id=self.external_id,
            external_name=self.external_name,
            badgr_entityID=self.badgr_entityID,
            issuer_id=self.issuer_id
        )
