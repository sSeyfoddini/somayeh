from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class BadgeTypeModel(db.Model):
    """
    Data model for BadgeType DB table.
    """

    __tablename__ = "badge_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    extrernal_partner_id = db.Column(db.String, nullable=True, index=True)
    extrernal_partner_label = db.Column(db.String, nullable=True, index=True)
    badge_org_type = db.Column(db.String, nullable=True, index=True)
    badge_org_id = db.Column(db.String, nullable=True, index=True)
    badge_org_label = db.Column(db.String, nullable=True, index=True)
    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=False)
    external_id = db.Column(db.String, nullable=True)
    reference_uri = db.Column(db.String, nullable=True)
    image = db.Column(db.JSON, nullable=True, default=None)
    attachment = db.Column(db.JSON, nullable=True, default=None)
    type = db.Column(db.String, nullable=True)
    json = db.Column(db.JSON, nullable=True)
    credential_type_uuid = db.Column(db.String, nullable=True)
    org_uuid = db.Column(db.String, nullable=True)
    entityID = db.Column(db.String, nullable=True)
    auto_issue = db.Column(db.Boolean, nullable=True, default=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "extrernal_partner_id": self.extrernal_partner_id,
            "extrernal_partner_label": self.extrernal_partner_label,
            "badge_org_type": self.badge_org_type,
            "badge_org_id": self.badge_org_id,
            "badge_org_label": self.badge_org_label,
            "name": self.name,
            "abbreviation": self.abbreviation,
            "description": self.description,
            "external_id": self.external_id,
            "reference_uri": self.reference_uri,
            "image":self.image,
            "attachment": self.attachment,
            "type": self.type,
            "json": self.json,
            "credential_type_uuid": self.credential_type_uuid,
            "org_uuid": self.org_uuid,
            "entityID": self.entityID,
            "auto_issue": self.auto_issue
        }

    def _clone(self):
        return BadgeTypeModel(
            uuid=self.uuid,
            extrernal_partner_id=self.extrernal_partner_id,
            extrernal_partner_label=self.extrernal_partner_label,
            badge_org_type=self.badge_org_type,
            badge_org_id=self.badge_org_id,
            badge_org_label=self.badge_org_label,
            name=self.name,
            abbreviation=self.abbreviation,
            description=self.description,
            external_id=self.external_id,
            reference_uri=self.reference_uri,
            image=self.image,
            attachment=self.attachment,
            type=self.type,
            json=self.json,
            credential_type_uuid=self.credential_type_uuid,
            org_uuid=self.org_uuid,
            entityID=self.entityID,
            auto_issue=self.auto_issue
        )
