from app import db
from uuid import uuid4

def uuid():
    return str(uuid4())

class SourceSkillTypeModel(db.Model):
    """
    Data model for SourceSkillType DB table.
    """

    __tablename__ = "source_skill_type"

    uuid = db.Column(db.String, primary_key=True, default=uuid)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    source_skill_library_id = db.Column(db.String, nullable=False, index=True)
    external_id = db.Column(db.String, nullable=False)
    reference_uri = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    occupations = db.Column(db.String, nullable=True)
    employer = db.Column(db.String, nullable=True)
    certifications = db.Column(db.String, nullable=True)
    keywords = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)

    def _to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "source_skill_library_id": self.source_skill_library_id,
            "external_id": self.external_id,
            "reference_uri": self.reference_uri,
            "category": self.category,
            "occupations": self.occupations,
            "employer": self.employer,
            "certifications": self.certifications,
            "keywords": self.keywords,
            "type": self.type,
        }

    def _clone(self):
        return SourceSkillTypeModel(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            source_skill_library_id=self.source_skill_library_id,
            external_id=self.external_id,
            reference_uri=self.reference_uri,
            category=self.category,
            occupations=self.occupations,
            employer=self.employer,
            certifications=self.certifications,
            keywords=self.keywords,
            type=self.type,
        )
