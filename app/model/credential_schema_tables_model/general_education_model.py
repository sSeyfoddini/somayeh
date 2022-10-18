from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class GeneralEducationModel(db.Model):
    """
    Data model for GeneralEducation DB table.
    """

    __tablename__ = "general_education"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    label = db.Column(db.String, nullable=False)
    college_id = db.Column(db.BIGINT, nullable=True, index=True)
    reference_uri = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String, nullable=False)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "abbreviation": self.abbreviation,
            "description": self.description,
            "label": self.label,
            "college_id": self.college_id,
            "reference_uri": self.reference_uri,
            "type": self.type,
            "external_id": self.external_id,
        }

    def _clone(self):
        return GeneralEducationModel(
            uuid=self.uuid,
            name=self.name,
            abbreviation=self.abbreviation,
            description=self.description,
            label=self.label,
            college_id=self.college_id,
            reference_uri=self.reference_uri,
            type=self.type,
            external_id=self.external_id,
        )
