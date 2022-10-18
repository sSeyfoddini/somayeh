from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class OrganizationIdentityModel(db.Model):
    """
    Data model for OrganizationIdentity DB table.
    """

    __tablename__ = "organization_identity"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    abbreviation = db.Column(db.String, nullable=True)
    credential_type_id = db.Column(db.String, nullable=True)
    organization_label = db.Column(db.String, nullable=False)
    organization_type_id = db.Column(db.BIGINT, nullable=True, index=True)
    organization_type_label = db.Column(db.String, nullable=True)
    organization_subtype_id = db.Column(db.BIGINT, nullable=True, index=True)
    organization_subtype_label = db.Column(db.String, nullable=True)
    organization_parent_id = db.Column(db.BIGINT, nullable=True)
    organization_parent_label = db.Column(db.String, nullable=True)
    logo = db.Column(db.String, nullable=True)
    background = db.Column(db.String, nullable=True)
    reference_url = db.Column(db.String, nullable=True)
    street_1 = db.Column(db.String, nullable=False)
    street_2 = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "abbreviation": self.abbreviation,
            "credential_type_id": self.credential_type_id,
            "organization_label": self.organization_label,
            "organization_type_id": self.organization_type_id,
            "organization_type_label": self.organization_type_label,
            "organization_subtype_id": self.organization_subtype_id,
            "organization_subtype_label": self.organization_subtype_label,
            "organization_parent_id": self.organization_parent_id,
            "organization_parent_label": self.organization_parent_label,
            "logo": self.logo,
            "background": self.background,
            "reference_url": self.reference_url,
            "street_1": self.street_1,
            "street_2": self.street_2,
            "country": self.country,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code,
            "type": self.type,
            "external_id": self.external_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return OrganizationIdentityModel(
            abbreviation=self.abbreviation,
            credential_type_id=self.credential_type_id,
            organization_label=self.organization_label,
            organization_type_id=self.organization_type_id,
            organization_type_label=self.organization_type_label,
            organization_subtype_id=self.organization_subtype_id,
            organization_subtype_label=self.organization_subtype_label,
            organization_parent_id=self.organization_parent_id,
            organization_parent_label=self.organization_parent_label,
            logo=self.logo,
            background=self.background,
            reference_url=self.reference_url,
            street_1=self.street_1,
            street_2=self.street_2,
            country=self.country,
            city=self.city,
            region=self.region,
            postal_code=self.postal_code,
            type=self.type,
            external_id=self.external_id,
            parent_organization=self.parent_organization,
            uuid=self.uuid,
        )
