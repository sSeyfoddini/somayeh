from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SkillCategoryModel(db.Model):
    """
    Data model for SkillCategory DB table.
    """

    __tablename__ = "skill_category"

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    reference_uri = db.Column(db.String, nullable=True)
    uuid = db.Column(db.String, primary_key=True, default=uuid)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "reference_uri": self.reference_uri
        }

    def _clone(self):
        return SkillCategoryModel(
            name=self.name, description=self.description, reference_uri=self.reference_uri, uuid=self.uuid
        )
