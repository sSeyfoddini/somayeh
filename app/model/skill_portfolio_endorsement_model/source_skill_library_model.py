from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SourceSkillLibraryModel(db.Model):
    """
    Data model for SourceSkillLibrary DB table.
    """

    __tablename__ = "source_skill_library"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    external_id = db.Column(db.String, nullable=False)
    reference_uri = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "external_id": self.external_id,
            "reference_uri": self.reference_uri,
            "type": self.type,
        }

    def _clone(self):
        return SourceSkillLibraryModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            external_id=self.external_id,
            reference_uri=self.reference_uri,
            type=self.type,
        )
