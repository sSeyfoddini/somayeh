from uuid import uuid4
from app import db


def uuid():
    return str(uuid4())


class OrganizationLevelModel(db.Model):
    """
    Data model for OrganizationLevel DB table
    """

    __tablename__ = "organization_level"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
        }

    def _clone(self):
        return OrganizationLevelModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
        )
