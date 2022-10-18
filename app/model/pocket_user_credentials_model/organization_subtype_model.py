from uuid import uuid4
from app import db


def uuid():
    return str(uuid4())


class OrganizationSubtypeModel(db.Model):
    """
    Data model for OrganizationSubtype DB table.
    """

    __tablename__ = "organization_subtype"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    subtype_id = db.Column(db.BIGINT, nullable=False)

    def _to_dict(self):
        return {"uuid": self.uuid, "name": self.name, "description": self.description, "subtype_id": self.subtype_id}

    def _clone(self):
        return OrganizationSubtypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            subtype_id=self.subtype_id,
        )
