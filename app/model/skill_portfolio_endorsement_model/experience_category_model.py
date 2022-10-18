from uuid import uuid4
from app import db


def uuid():
    return str(uuid4())


class ExperienceCategoryModel(db.Model):
    """
    Data model for Experience Category DB table.
    """

    __tablename__ = "experience_category"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    parent_name = db.Column(db.String, nullable=True)
    parent_id = db.Column(db.BIGINT, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "parent_name": self.parent_name,
            "parent_id": self.parent_id,
        }

    def _clone(self):
        return ExperienceCategoryModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            parent_name=self.parent_name,
            parent_id=self.parent_id,
        )
