from sqlalchemy import ForeignKey

from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class CredentialTypeModel(db.Model):
    """
    Data model for CredentialType DB table.
    """

    __tablename__ = "credential_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    """credential_definition_uuid = db.Column(
        db.String, ForeignKey("badge_type.credential_type_uuid", onupdate="CASCADE", ondelete="CASCADE"), nullable=True
    )"""
    credential_definition_uuid = db.Column(
        db.String, nullable=True
    )
    name = db.Column(db.String, nullable=False)
    credential_type = db.Column(db.String, nullable=True)
    schema_uri = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "credential_definition_uuid": self.credential_definition_uuid,
            "name": self.name,
            "credential_type": self.credential_type,
            "schema_uri": self.schema_uri,
        }

    def _clone(self):
        return CredentialTypeModel(
            credential_definition_uuid=self.credential_definition_uuid,
            name=self.name,
            credential_type=self.credential_type,
            uuid=self.uuid,
            schema_uri=self.schema_uri,
        )
