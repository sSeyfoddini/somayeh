from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class TitleModel(db.Model):
    """
    Data model for Title DB table.
    """

    __tablename__ = "title"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    credential_type_id = db.Column(db.String, nullable=False)
    credential_type_label = db.Column(db.String, nullable=True)
    title_type_id = db.Column(db.BIGINT, nullable=False)
    title_type_label = db.Column(db.String, nullable=False)
    organization_id = db.Column(db.String, nullable=False)
    organization_label = db.Column(db.String, nullable=False)
    conferral_date = db.Column(db.DateTime(timezone=False), nullable=False)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_type_id": self.credential_type_id,
            "credential_type_label": self.credential_type_label,
            "title_type_id": self.title_type_id,
            "title_type_label": self.title_type_label,
            "organization_id": self.organization_id,
            "organization_label": self.organization_label,
            "conferral_date": str(self.conferral_date),
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return TitleModel(
            uuid=self.uuid,
            credential_type_id=self.credential_type_id,
            credential_type_label=self.credential_type_label,
            title_type_id=self.title_type_id,
            title_type_label=self.title_type_label,
            organization_id=self.organization_id,
            organization_label=self.organization_label,
            conferral_date=self.conferral_date,
            type=self.type,
            external_id=self.external_id,
        )
