from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class RoleModel(db.Model):
    """
    Data model for Role DB table.
    """

    __tablename__ = "role"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)
    credential_type_id = db.Column(db.String, nullable=True)
    parent_organization = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "type": self.type,
            "external_id": self.external_id,
            "credential_type_id": self.credential_type_id,
            "parent_organization": self.parent_organization,
        }

    def _clone(self):
        return RoleModel(
            uuid=self.uuid,
            name=self.name,
            type=self.type,
            external_id=self.external_id,
            credential_type_id=self.credential_type_id,
            parent_organization=self.parent_organization,
        )
